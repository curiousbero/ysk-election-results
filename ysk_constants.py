import dataclasses
@dataclasses.dataclass
class YSKElectionTypes:
    PRESIDENTIAL: int = 9
    REFERENDUM : int = 0
    PARLIAMENTARY: int = 8
    LOCAL_METROPOLITAN_MAYOR: int = 0
    LOCAL_MAYOR: int = 0
    LOCAL_DISTRICT_MAYOR: int = 0
    LOCAL_CITY_PARLIAMENT: int = 0
    LOCAL_DISTRICT_PARLIAMENT: int = 0
    PRESIDENTIAL_RUNOFF: int = 0

@dataclasses.dataclass
class YSKElections:
    GENERAL_2018: int = 16300
    GENERAL_2023: int = 20230
    PRESIDENTAL_2023: int = 20240 # 28th may

@dataclasses.dataclass
class YSKIsDomestic:
    YES: int = 1
    NO: int = 0
