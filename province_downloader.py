import json
import time
import datetime
import requests
import api_caller   
import ysk_constants
from globals import print_and_log, ELECTION, ysk, search_in_dict_list

time.sleep(4)
provinces = ysk.get_province_list(ELECTION, ysk_constants.YSKElectionTypes.PARLIAMENTARY)
provinces_sanitized = []
for index, province in enumerate(provinces):
    index = search_in_dict_list(provinces_sanitized, "id", province["il_ID"])
    if index == -1:
        provinces_sanitized.append({"name": province["il_ADI"], "id": province["il_ID"], "electoral_regions": [], "districts": []})
        index = len(provinces_sanitized) - 1
    provinces_sanitized[index]["electoral_regions"].append(province["secim_CEVRESI_ID"])
    print_and_log(f"Added {province['il_ADI']} to the list of provinces.")

for province in provinces_sanitized:
    for electoral_region_id in province["electoral_regions"]:
        districts = ysk.get_district_list(province["id"], ELECTION, ysk_constants.YSKElectionTypes.PARLIAMENTARY, electoral_region_id)
        for district in districts:
            province["districts"].append({"name": district["ilce_ADI"], "id": district["ilce_ID"], "electoral_region_id": electoral_region_id})
        print_and_log(f"Added {len(districts)} districts to the list of districts in {province['name']}(with ID {province['id']}, electoral region {electoral_region_id})")
        print_and_log(f"Sleeping for 4 seconds to avoid rate limiting.")
        time.sleep(4)

with open("provinces.json", "w", encoding="utf-8") as provinces_file:
    json.dump(provinces_sanitized, provinces_file, indent=4, ensure_ascii=False)
    print_and_log(f"Saved the list of provinces to provinces.json")


