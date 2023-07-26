from irslashdata import constants as ct

from irslashdata import logger
from irslashdata.helpers import encode_password
from .exceptions import AuthenticationError, ServerDownError, ForbiddenError, IracingError, BadRequestError, NotFoundError

from datetime import datetime, timezone
import httpx
import asyncio
import json


# This module authenticates a session, builds a URL query from parameters,
# and returns data in easily digestible forms.
# Cookies are handled by the httpx module behind the scenes and are not
# written to file.

# Authentication happens automatically on the first method call from Client().
# When a request fails from an expired cookie, a re-auth is triggered and
# the last request that failed is tried again.


class Client:
    def __init__(self, username: str, password: str):
        """ This class is used to interact with all iRacing endpoints that
        have been discovered so far. After creating an instance of Client
        it is required to call authenticate(), due to async limitations.

        An alternative to storing credentials as string in the class arguments
        is to store then in your OS environment and call with os.getenv().
        """
        self.username = username
        self.password = encode_password(username, password)
        self.session = httpx.AsyncClient()
        self.maintenance_lock = False

    async def _authenticate(self):
        """ Sends a POST request to iRacings login server, initiating a
        persistent connection stored in self.session
        """
        logger.info('Authenticating...')

        login_data = {
            'email': self.username,
            'password': self.password
        }

        try:
            auth_response = await self.session.post(ct.URL_AUTH, data=login_data)
            auth_response.raise_for_status()
            response_content = json.loads(auth_response.text)
            if 'authcode' in response_content:
                if response_content['authcode'] == 0:
                    message = "Error: No authcode returned in authorization request."
                    if 'message' in response_content:
                        message += "Reason: " + response_content['message']

                    logger.warning(message)
                    raise AuthenticationError(message, auth_response)

        except httpx.RequestError as exc:
            logger.warning("Bad request when trying to authenticate.")
            raise BadRequestError("Bad request when trying to authenticate.", exc.request)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 400:
                logger.warning('400 Bad request during authentication. URL: ' + exc.request.url)
                raise BadRequestError("400 Bad request during authentication.", exc.request)
            if exc.response.status_code == 401:
                logger.warning(
                    'The login POST request returned status code 401 '
                    'indicating an authentication failure. Please check '
                    'the supplied credentials.')
                raise AuthenticationError('Login Failed: Authentication failure.', exc.response)
            elif exc.response.status_code == 503:
                logger.warning(
                    'The iRacing stats server is currently down for maintenance.')
                raise ServerDownError('Login Failed: iRacing is down for maintenance.', exc.response)
            else:
                try:
                    auth_response_json = exc.response.json()
                except json.decoder.JSONDecodeError:
                    auth_response_json = 'Error: response json could not be decoded.'

                logger.warning(
                    'The following unhandled response code was received from the '
                    'server: ' + str(auth_response.status_code) + "\n"
                    'Here is the complete response json: \n' + auth_response_json)
                raise IracingError('Login Failed: Unknown error.', exc.response)
        else:
            logger.info("Successfully logged into iRacing /data server.")

    async def _build_request(self, url, params):
        """ Builds the final GET request from url and params
        """
        if not self.session.cookies.__bool__():
            logger.info("No cookies in cookie jar.")
            try:
                await self._authenticate()
            except (AuthenticationError, IracingError, ServerDownError, BadRequestError):
                raise

        logger.info(f'Request being sent to: {url} with params: {json.dumps(params)}')

        try:
            response = await self.session.get(
                url,
                params=params,
                follow_redirects=False,
                timeout=None
            )
            response.raise_for_status()
            return response
        except httpx.RequestError as exc:
            raise BadRequestError("Bad request. URL: " + exc.request.url, exc.request)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 400:
                try:
                    response_json = exc.response.json()
                except json.decoder.JSONDecodeError:
                    response_json = 'Error: json could not be decoded.'

                logger.error(f'400: Bad request. Response from iRacing:\n{response_json}')
                raise BadRequestError('Error: Bad request.', exc.response)
            elif exc.response.status_code == 401:
                logger.info(
                    '401: Unauthorized. The cookies are likely expired. '
                    'Initiating re-authentication.'
                )
                try:
                    await self._authenticate()
                except (AuthenticationError, IracingError, ServerDownError, BadRequestError) as exc:
                    logger.info("Abandoning request. Could not re-authenticate.")
                    raise AuthenticationError("Abandoning request. Could not re-authenticate.", exc.response)
                else:
                    logger.info("Retrying request.")
                    return await self._build_request(url, params)
            elif exc.response.status_code == 403:
                # Forbidden!
                logger.warning("403 Forbidden: This iRacing user account is forbidden from accessing this data.")
                raise ForbiddenError("403 forbidden. This iRacing user account is forbidden from accessing this data.", exc.response)
            elif exc.response.status_code == 404:
                # Not found!
                logger.warning("404 Not found: The requested data was not found.")
                raise NotFoundError("404 not found: The requested data was not found.", exc.response)
            elif exc.response.status_code == 408:
                logger.warning('408: Request timed out.')
                raise IracingError("408: Request timed out.", exc.response)
            elif exc.response.status_code == 503:
                logger.warning("503: The iRacing stats server is currently down for maintenance.")
                raise ServerDownError("503: The iRacing stats server is currently down for maintenance.", exc.response)
            else:
                try:
                    response_json = response.json()
                except json.decoder.JSONDecodeError:
                    response_json = 'Error: response json could not be decoded.'

                logger.warning(
                    'The following unhandled response code was received from the '
                    'server: ' + str(response.status_code) + "\n"
                    'Here is the complete response json: \n' + response_json)
                raise IracingError('Request Failed: Unknown error.', exc.response)

    async def get_data(self, url, parameters):
        try:
            response_ir = await self._build_request(url, parameters)
        except (ServerDownError, AuthenticationError):
            raise
        except IracingError:
            return None

        if response_ir is None:
            return None

        response_ir_json = response_ir.json()

        rate_limit_remaining = response_ir.headers['x-ratelimit-remaining']
        rate_limit_reset = int(response_ir.headers['x-ratelimit-reset'])
        now = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        time_to_reset = int(rate_limit_reset - now)
        for i in range(3 - len(rate_limit_remaining)):
            rate_limit_remaining = ' ' + rate_limit_remaining
        logger.info(f"rate_limit_remaining: {rate_limit_remaining}")
        if int(rate_limit_remaining) < 50:
            logger.info(f"Approaching rate limit. Sleeping http requests for {time_to_reset} seconds")
            await asyncio.sleep(time_to_reset)

        data = []

        if 'link' in response_ir_json:
            try:
                response_amazon = await self._build_request(response_ir_json['link'], {})
            except (ServerDownError, AuthenticationError):
                raise
            except IracingError:
                return None

            if response_amazon is None:
                return None

            if isinstance(response_amazon.json(), list):
                data = response_amazon.json()
            else:
                data.append(response_amazon.json())
        elif 'data' in response_ir_json and 'chunk_info' in response_ir_json['data'] and 'chunk_file_names' in response_ir_json['data']['chunk_info']:
            for chunk_filename in response_ir_json['data']['chunk_info']['chunk_file_names']:
                chunk_url = response_ir_json['data']['chunk_info']['base_download_url'] + chunk_filename

                try:
                    response_amazon = await self._build_request(chunk_url, {})
                except (ServerDownError, AuthenticationError):
                    raise
                except IracingError:
                    return None

                for item in response_amazon.json():
                    data.append(item)
        else:
            data = response_ir_json

        return data

    async def search_results_new(
        self,
        season_year=None,
        season_quarter=None,
        start_range_begin=None,
        start_range_end=None,
        finish_range_begin=None,
        finish_range_end=None,
        cust_id=None,
        team_id=None,
        series_id=None,
        race_week_num=None,
        official_only=None,
        event_types=[5],
        category_ids=[1, 2, 3, 4]
    ):
        """ Returns a list with a SearchResults object for each of a driver's
        past events that meet the selected criteria. You must provide either a year
        and quarter or a time range with starttime_low and starttime_high. Default
        is to return results from race events in any category and any series.
        """
        parameters = {}

        if cust_id is not None:
            parameters['cust_id'] = cust_id

        if team_id is not None:
            parameters['team_id'] = team_id

        if series_id is not None:
            parameters['series_id'] = series_id

        if race_week_num is not None:
            parameters['race_week_num'] = race_week_num

        if official_only is not None:
            parameters['official_only'] = official_only

        if event_types is not None:
            parameters['event_types'] = event_types

        if category_ids is not None:
            parameters['category_ids'] = category_ids

        if season_year is not None and season_quarter is not None:
            parameters['season_year'] = season_year
            parameters['season_quarter'] = season_quarter
        elif start_range_begin is not None:
            parameters['start_range_begin'] = start_range_begin
            if start_range_end is not None:
                parameters['start_range_end'] = start_range_end
        elif finish_range_begin is not None:
            parameters['finish_range_begin'] = finish_range_begin
            if finish_range_end is not None:
                parameters['finish_range_end'] = finish_range_end
        else:
            logger.warning("You must either supply season_year and season_quarter, start_range_begin, or finish_range_begin.")
            raise ValueError("You must either supply season_year and season_quarter, start_range_begin, or finish_range_begin.")
        url = 'https://members-ng.iracing.com/data/results/search_series'
        try:
            results = await self.get_data(url, parameters)
            if results is None:
                results = []
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            results = []

        return results

    async def search_hosted_new(
        self,
        start_range_begin=None,
        start_range_end=None,
        finish_range_begin=None,
        finish_range_end=None,
        cust_id=None,
        team_id=None,
        host_cust_id=None,
        session_name=None,
        league_id=None,
        league_season_id=None,
        car_id=None,
        track_id=None,
        category_ids=[1, 2, 3, 4]
    ):
        """ Returns a list with a SearchResults object for each of a driver's
        past events that meet the selected criteria. You must provide either a year
        and quarter or a time range with starttime_low and starttime_high. Default
        is to return results from race events in any category and any series.
        """
        parameters = {}

        if cust_id is not None:
            parameters['cust_id'] = cust_id
        elif team_id is not None:
            parameters['team_id'] = team_id
        elif host_cust_id is not None:
            parameters['host_cust_id'] = host_cust_id
        elif session_name is not None:
            parameters['session_name'] = session_name
        else:
            logger.warning("You must supply one of cust_id, team_id, host_cust_id, or session_name to search hosted results.")
            return []

        if league_id is not None:
            parameters['league_id'] = league_id

        if league_season_id is not None:
            parameters['league_season_id'] = league_season_id

        if car_id is not None:
            parameters['car_id'] = car_id

        if track_id is not None:
            parameters['track_id'] = track_id

        if category_ids is not None:
            parameters['category_ids'] = category_ids

        if start_range_begin is not None:
            parameters['start_range_begin'] = start_range_begin
            if start_range_end is not None:
                parameters['start_range_end'] = start_range_end
        elif finish_range_begin is not None:
            parameters['finish_range_begin'] = finish_range_begin
            if finish_range_end is not None:
                parameters['finish_range_end'] = finish_range_end
        else:
            logger.warning("You must either supply start_range_begin or finish_range_begin.")
            return []
        url = 'https://members-ng.iracing.com/data/results/search_hosted'
        try:
            results = await self.get_data(url, parameters)
            if results is None:
                results = []
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            results = []

        return results

    async def stats_series_new(self):
        """ Returns a list of dicts containing data about each series ever run in iRacing.
        """
        parameters = {}

        url = 'https://members-ng.iracing.com/data/series/stats_series'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            results = []

        return results

    async def current_race_week_new(
        self,
        series_id: int = 139
    ):
        """ Returns a tuple of (season_year, season_quarter, race_week, max_weeks, active)
        Returns None if the series is not current.
        """
        parameters = {}

        season_year = None
        season_quarter = None
        race_week = None
        max_weeks = None
        active = None

        url = 'https://members-ng.iracing.com/data/series/seasons'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            return (None, None, None, None, None)

        for series in results:
            if 'series_id' in series and series['series_id'] == series_id:
                if 'season_year' in series:
                    season_year = series['season_year']

                if 'season_quarter' in series:
                    season_quarter = series['season_quarter']

                if 'race_week' in series:
                    race_week = series['race_week']

                if 'max_weeks' in series:
                    max_weeks = series['max_weeks']

                if 'active' in series:
                    active = series['active']

                return (season_year, season_quarter, race_week, max_weeks, active)

        return (None, None, None, None, None)

    async def subsession_data_new(
        self,
        subsession_id
    ):
        """ Returns a dict with all the information about the subsession indicated by subsession_id.
        """
        parameters = {
            'subsession_id': subsession_id,
            'include_licenses': True
        }

        url = 'https://members-ng.iracing.com/data/results/get'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            return None

        if results is None or len(results) < 1:
            return None

        if len(results) > 1:
            logger.warning(f'subsession_data_new returned more than one race dict. Returning the first in the list.')

        return results[0]

    async def get_member_info_new(
        self,
        cust_ids: list
    ):
        """ Returns a list of dicts containing information about iRacing members.
        cust_ids: list containing the iRacing cust_ids of the members being looked up.
        """
        parameters = {
            'cust_ids': cust_ids
        }

        url = 'https://members-ng.iracing.com/data/member/get'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            return None

        if results is None or len(results) < 1:
            return None

        if 'success' not in results[0] or results[0]['success'] is False:
            return None

        if 'members' not in results[0]:
            return None

        return results[0]['members']

    async def lookup_drivers_new(
        self,
        search_string: str,
        league_id: int = None
    ):
        parameters = {
            'search_term': search_string,
            'league_id': league_id
        }

        url = 'https://members-ng.iracing.com/data/lookup/drivers'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            results = []

        return results

    async def current_seasons_new(
            self,
            include_series: bool = True
    ):
        """ Returns a list with a SearchResults object for each of a driver's
        past events that meet the selected criteria. You must provide either a year
        and quarter or a time range with starttime_low and starttime_high. Default
        is to return results from race events in any category and any series.
        """

        parameters = {
            'include_series': include_series
        }

        url = 'https://members-ng.iracing.com/data/series/seasons'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            return None

        if results is None or len(results) < 1:
            return None

        return results

    async def current_car_classes_new(
        self
    ):
        """ Returns a list of current car_class dicts
        """
        parameters = {
        }

        url = 'https://members-ng.iracing.com/data/carclass/get'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            return None

        if results is None or len(results) < 1:
            return None

        return results

    async def chart_data_new(
        self,
        cust_id,
        category_id=2,
        chart_type=1
    ):
        """ Returns a list of (timestamp, value) tuples containing the requested data.
        """
        parameters = {
            'cust_id': cust_id,
            'category_id': category_id,
            'chart_type': chart_type
        }

        url = 'https://members-ng.iracing.com/data/member/chart_data'

        try:
            results = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            return None

        if results is None or len(results) < 1:
            return None

        if 'data' not in results[0]:
            return None

        if 'success' not in results[0] or results[0]['success'] is not True:
            return None

        return results[0]['data']

    async def race_guide_new(
        self,
        from_time: str = None,
        include_end_after_time: bool = None
    ):
        parameters = {}

        if from_time is not None:
            parameters['from'] = from_time

        if include_end_after_time is not None:
            parameters['include_end_after_time'] = include_end_after_time

        url = 'https://members-ng.iracing.com/data/season/race_guide'

        try:
            response = await self.get_data(url, parameters)
        except (AuthenticationError, ServerDownError):
            raise
        except IracingError:
            return None

        if response is None or len(response) < 1:
            return None

        if response[0] is None or response[0] == {}:
            return None

        if 'sessions' not in response[0]:
            return None

        if 'success' not in response[0] or response[0]['success'] is not True:
            return None

        return response[0]
