# _*_ coding: utf_8 _*_
from enum import Enum


class License(Enum):
    R = 1
    D = 2
    C = 3
    B = 4
    A = 5
    P = 6
    PWC = 7


class Category(Enum):
    """Holds the index for each type of racing discipline
    """
    oval = 1
    road = 2
    dirt_oval = 3
    dirt_road = 4


class ChartType(Enum):
    """Holds the index for the charts available from stats_chart()
    """
    irating = 1
    ttrating = 2
    license_class = 3


class EventType(Enum):
    """Holds the index for the session event type
    """
    # test = 1 (deprecated)
    practice = 2
    qualify = 3
    time_trial = 4
    race = 5
    # official = 6 (deprecated)
    # unofficial = 7 (deprecated)


class SimSessionType(Enum):
    race = 6
    open_qualifying = 5
    lone_qualifying = 4
    open_practice = 3


class IncFlags(Enum):
    clean = 0
    pitted = 2
    off_track = 4
    black_flag = 8
    car_reset = 16
    contact = 32
    car_contact = 64
    lost_control = 128
    discontinuity = 256
    interpolated_crossing = 512
    clock_smash = 1024
    tow = 2048


class Sort(Enum):
    """Holds the strings used for types of 'sort by'
    """
    irating = 'irating'
    start_time = 'start_time'
    champ_points = 'points'
    descending = 'desc'
    ascending = 'asc'
    session_name = 'sessionname'


# TODO Construct dictionary of seriesIDs from /GetSeasons
# TODO Construct dictionary of seasonIDs from /GetSeasons
# TODO Construct dictionary of carIDs


class SessionStatus(Enum):
    registered = 1
    do_not_join = 2
    ok_to_join = 3
    joined = 4
    assigned = 5
    withdrawn = 6
    rejected = 7


class CountryCodes(Enum):
    """Hold the string index of Country Codes that
    iRacing uses for seperating drivers into clubs
    """
    ALL = 'null'
    AFGHANISTAN = 'AF'
    ALAND_ISLANDS = 'AX'
    ALBANIA = 'AL'
    ALGERIA = 'DZ'
    AMERICAN_SAMOA = 'AS'
    ANDORRA = 'AD'
    ANGOLA = 'AO'
    ANGUILLA = 'AI'
    ANTARCTICA = 'AQ'
    ANTIGUA_AND_BARBUDA = 'AG'
    ARGENTINA = 'AR'
    ARMENIA = 'AM'
    ARUBA = 'AW'
    AUSTRALIA = 'AU'
    AUSTRIA = 'AT'
    AZERBAIJAN = 'AZ'
    BAHAMAS = 'BS'
    BAHRAIN = 'BH'
    BANGLADESH = 'BD'
    BARBADOS = 'BB'
    BELARUS = 'BY'
    BELGIUM = 'BE'
    BELIZE = 'BZ'
    BENIN = 'BJ'
    BERMUDA = 'BM'
    BHUTAN = 'BT'
    BOLIVIA_PLURINATIONAL_STATE_OF = 'BO'
    BOSNIA_AND_HERZEGOVINA = 'BA'
    BOTSWANA = 'BW'
    BOUVET_ISLAND = 'BV'
    BRAZIL = 'BR'
    BRITISH_INDIAN_OCEAN_TERRITORY = 'IO'
    BRUNEI_DARUSSALAM = 'BN'
    BULGARIA = 'BG'
    BURKINA_FASO = 'BF'
    BURUNDI = 'BI'
    CAMBODIA = 'KH'
    CAMEROON = 'CM'
    CANADA = 'CA'
    CAPE_VERDE = 'CV'
    CAYMAN_ISLANDS = 'KY'
    CENTRAL_AFRICAN_REPUBLIC = 'CF'
    CHAD = 'TD'
    CHILE = 'CL'
    CHINA = 'CN'
    CHRISTMAS_ISLAND = 'CX'
    COCOS_KEELING_ISLANDS = 'CC'
    COLOMBIA = 'CO'
    COMOROS = 'KM'
    CONGO = 'CG'
    CONGO_THE_DEMOCRATIC_REPUBLIC_OF_THE = 'CD'
    COOK_ISLANDS = 'CK'
    COSTA_RICA = 'CR'
    COTE_DIVOIRE = 'CI'
    CROATIA = 'HR'
    CUBA = 'CU'
    CYPRUS = 'CY'
    CZECH_REPUBLIC = 'CZ'
    DENMARK = 'DK'
    DJIBOUTI = 'DJ'
    DOMINICA = 'DM'
    DOMINICAN_REPUBLIC = 'DO'
    ECUADOR = 'EC'
    EGYPT = 'EG'
    EL_SALVADOR = 'SV'
    EQUATORIAL_GUINEA = 'GQ'
    ERITREA = 'ER'
    ESTONIA = 'EE'
    ETHIOPIA = 'ET'
    FALKLAND_ISLANDS_MALVINAS = 'FK'
    FAROE_ISLANDS = 'FO'
    FIJI = 'FJ'
    FINLAND = 'FI'
    FRANCE = 'FR'
    FRENCH_GUIANA = 'GF'
    FRENCH_POLYNESIA = 'PF'
    FRENCH_SOUTHERN_TERRITORIES = 'TF'
    GABON = 'GA'
    GAMBIA = 'GM'
    GEORGIA = 'GE'
    GERMANY = 'DE'
    GHANA = 'GH'
    GIBRALTAR = 'GI'
    GREECE = 'GR'
    GREENLAND = 'GL'
    GRENADA = 'GD'
    GUADELOUPE = 'GP'
    GUAM = 'GU'
    GUATEMALA = 'GT'
    GUERNSEY = 'GG'
    GUINEA = 'GN'
    GUINEA_BISSAU = 'GW'
    GUYANA = 'GY'
    HAITI = 'HT'
    HEARD_ISLAND_AND_MCDONALD_ISLANDS = 'HM'
    HOLY_SEE_VATICAN_CITY_STATE = 'VA'
    HONDURAS = 'HN'
    HONG_KONG = 'HK'
    HUNGARY = 'HU'
    ICELAND = 'IS'
    INDIA = 'IN'
    INDONESIA = 'ID'
    IRAN_ISLAMIC_REPUBLIC_OF = 'IR'
    IRAQ = 'IQ'
    IRELAND = 'IE'
    ISLE_OF_MAN = 'IM'
    ISRAEL = 'IL'
    ITALY = 'IT'
    JAMAICA = 'JM'
    JAPAN = 'JP'
    JERSEY = 'JE'
    JORDAN = 'JO'
    KAZAKHSTAN = 'KZ'
    KENYA = 'KE'
    KIRIBATI = 'KI'
    KOREA_DEMOCRATIC_PEOPLES_REPUBLIC_OF = 'KP'
    KOREA_REPUBLIC_OF = 'KR'
    KUWAIT = 'KW'
    KYRGYZSTAN = 'KG'
    LAO_PEOPLES_DEMOCRATIC_REPUBLIC = 'LA'
    LATVIA = 'LV'
    LEBANON = 'LB'
    LESOTHO = 'LS'
    LIBERIA = 'LR'
    LIBYAN_ARAB_JAMAHIRIYA = 'LY'
    LIECHTENSTEIN = 'LI'
    LITHUANIA = 'LT'
    LUXEMBOURG = 'LU'
    MACAO = 'MO'
    MACEDONIA_THE_FORMER_YUGOSLAV_REPUBLIC_OF = 'MK'
    MADAGASCAR = 'MG'
    MALAWI = 'MW'
    MALAYSIA = 'MY'
    MALDIVES = 'MV'
    MALI = 'ML'
    MALTA = 'MT'
    MARSHALL_ISLANDS = 'MH'
    MARTINIQUE = 'MQ'
    MAURITANIA = 'MR'
    MAURITIUS = 'MU'
    MAYOTTE = 'YT'
    MEXICO = 'MX'
    MICRONESIA_FEDERATED_STATES_OF = 'FM'
    MOLDOVA_REPUBLIC_OF = 'MD'
    MONACO = 'MC'
    MONGOLIA = 'MN'
    MONTENEGRO = 'ME'
    MONTSERRAT = 'MS'
    MOROCCO = 'MA'
    MOZAMBIQUE = 'MZ'
    MYANMAR = 'MM'
    NAMIBIA = 'NA'
    NAURU = 'NR'
    NEPAL = 'NP'
    NETHERLANDS = 'NL'
    NETHERLANDS_ANTILLES = 'AN'
    NEW_CALEDONIA = 'NC'
    NEW_ZEALAND = 'NZ'
    NICARAGUA = 'NI'
    NIGER = 'NE'
    NIGERIA = 'NG'
    NIUE = 'NU'
    NORFOLK_ISLAND = 'NF'
    NORTHERN_MARIANA_ISLANDS = 'MP'
    NORWAY = 'NO'
    OMAN = 'OM'
    PAKISTAN = 'PK'
    PALAU = 'PW'
    PALESTINIAN_TERRITORY_OCCUPIED = 'PS'
    PANAMA = 'PA'
    PAPUA_NEW_GUINEA = 'PG'
    PARAGUAY = 'PY'
    PERU = 'PE'
    PHILIPPINES = 'PH'
    PITCAIRN = 'PN'
    POLAND = 'PL'
    PORTUGAL = 'PT'
    PUERTO_RICO = 'PR'
    QATAR = 'QA'
    REUNION = 'RE'
    ROMANIA = 'RO'
    RUSSIAN_FEDERATION = 'RU'
    RWANDA = 'RW'
    SAINT_BARTHELEMY = 'BL'
    SAINT_HELENA_ASCENSION_AND_TRISTAN_DA_CUNHA = 'SH'
    SAINT_KITTS_AND_NEVIS = 'KN'
    SAINT_LUCIA = 'LC'
    SAINT_MARTIN_FRENCH_PART = 'MF'
    SAINT_PIERRE_AND_MIQUELON = 'PM'
    SAINT_VINCENT_AND_THE_GRENADINES = 'VC'
    SAMOA = 'WS'
    SAN_MARINO = 'SM'
    SAO_TOME_AND_PRINCIPE = 'ST'
    SAUDI_ARABIA = 'SA'
    SENEGAL = 'SN'
    SERBIA = 'RS'
    SEYCHELLES = 'SC'
    SIERRA_LEONE = 'SL'
    SINGAPORE = 'SG'
    SLOVAKIA = 'SK'
    SLOVENIA = 'SI'
    SOLOMON_ISLANDS = 'SB'
    SOMALIA = 'SO'
    SOUTH_AFRICA = 'ZA'
    SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS = 'GS'
    SPAIN = 'ES'
    SRI_LANKA = 'LK'
    SUDAN = 'SD'
    SURINAME = 'SR'
    SVALBARD_AND_JAN_MAYEN = 'SJ'
    SWAZILAND = 'SZ'
    SWEDEN = 'SE'
    SWITZERLAND = 'CH'
    SYRIAN_ARAB_REPUBLIC = 'SY'
    TAIWAN_PROVINCE_OF_CHINA = 'TW'
    TAJIKISTAN = 'TJ'
    TANZANIA_UNITED_REPUBLIC_OF = 'TZ'
    THAILAND = 'TH'
    TIMOR_LESTE = 'TL'
    TOGO = 'TG'
    TOKELAU = 'TK'
    TONGA = 'TO'
    TRINIDAD_AND_TOBAGO = 'TT'
    TUNISIA = 'TN'
    TURKEY = 'TR'
    TURKMENISTAN = 'TM'
    TURKS_AND_CAICOS_ISLANDS = 'TC'
    TUVALU = 'TV'
    UGANDA = 'UG'
    UKRAINE = 'UA'
    UNITED_ARAB_EMIRATES = 'AE'
    UNITED_KINGDOM = 'GB'
    UNITED_STATES = 'US'
    UNITED_STATES_MINOR_OUTLYING_ISLANDS = 'UM'
    URUGUAY = 'UY'
    UZBEKISTAN = 'UZ'
    VANUATU = 'VU'
    VENEZUELA_BOLIVARIAN_REPUBLIC_OF = 'VE'
    VIET_NAM = 'VN'
    VIRGIN_ISLANDS_BRITISH = 'VG'
    VIRGIN_ISLANDS_US = 'VI'
    WALLIS_AND_FUTUNA = 'WF'
    WESTERN_SAHARA = 'EH'
    YEMEN = 'YE'
    ZAMBIA = 'ZM'
    ZIMBABWE = 'ZW'
