from globals import print_and_log, ELECTION, ysk, search_in_dict_list
import json
import time
import ysk_constants

with open("provinces.json", "r", encoding="utf-8") as f:
    provinces = json.load(f)

presidential_column_names = ysk.get_columns(ELECTION, ysk_constants.YSKElectionTypes.PRESIDENTIAL, 1)
parliamentary_column_names = ysk.get_columns(ELECTION, ysk_constants.YSKElectionTypes.PARLIAMENTARY, 1)
for province_index, province in enumerate(provinces):
    for district_index, district in enumerate(province["districts"]):
        president_result = None
        while president_result == None:
            try:
                president_result = ysk.get_ballot_boxes(ELECTION, ysk_constants.YSKElectionTypes.PRESIDENTIAL, province["id"], district["id"], ysk_constants.YSKIsDomestic.YES)
            except Exception as e:
                print_and_log(f"Error while getting presidential ballot boxes for {district['name']} with ID {district['id']} in {province['name']} with ID {province['id']}: {e}")
                print_and_log(f"Sleeping for 30 seconds for the next try.")
                time.sleep(30)
        columns_created = []
        for presidential_column_name in presidential_column_names:
            for ballot_box in president_result:
                if presidential_column_name["column_NAME"] in ballot_box:
                    ballot_box[presidential_column_name["ad"]] = ballot_box[presidential_column_name["column_NAME"]]
                    del ballot_box[presidential_column_name["column_NAME"]]
                    columns_created.append(presidential_column_name["ad"])
        district["neighborhoods"] = []
        for ballot_box in president_result:
            neighborhood_index = search_in_dict_list(district["neighborhoods"], "id", ballot_box["muhtarlik_ID"])
            if neighborhood_index == -1:
                district["neighborhoods"].append({"name": ballot_box["muhtarlik_ADI"], "id": ballot_box["muhtarlik_ID"], "ballot_boxes": {}})
                neighborhood_index = len(district["neighborhoods"]) - 1
            # The list of ballot boxes is created when we get the presidential results right here.
            # Given the ballot #'s and metadata(the # of registered voters) don't change, we can use the same list for parliamentary results.
            sanitized_ballot_box = {
                "number": ballot_box["sandik_NO"],
                "registered_voters": ballot_box["secmen_SAYISI"],
                "presidential_results": {
                    "valid_votes": 0,
                    "spoilt_votes": 0,
                    "total_votes": 0,
                    "numbers": {},
                    "percentages": {}
                },
                "parliamentary_results": {
                    "valid_votes": 0,
                    "spoilt_votes": 0,
                    "total_votes": 0,
                    "numbers": {},
                    "percentages": {}
                }
            }
            presidential_results = sanitized_ballot_box["presidential_results"]
            presidential_results["total_votes"] = ballot_box["gecerli_OY_TOPLAMI"] + ballot_box["gecersiz_OY_TOPLAMI"]
            presidential_results["valid_votes"] = ballot_box["gecerli_OY_TOPLAMI"]
            presidential_results["spoilt_votes"] = ballot_box["gecersiz_OY_TOPLAMI"]
            for column_created in columns_created:
                presidential_results["numbers"][column_created] = ballot_box[column_created]
                if presidential_results["valid_votes"] > 0:
                    presidential_results["percentages"][column_created] = round((ballot_box[column_created] / presidential_results["valid_votes"])*100, 4)
            district["neighborhoods"][neighborhood_index]["ballot_boxes"][ballot_box["sandik_NO"]] = sanitized_ballot_box
        print_and_log(f"Added {len(president_result)} presidential ballot boxes to the list of ballot boxes in {district['name']} with ID {district['id']} in {province['name']} with ID {province['id']} (district {district_index + 1}/{len(province['districts'])}, province {province_index + 1}/{len(provinces)})")
        print_and_log(f"Sleeping for 3 seconds to avoid rate limiting.")
        time.sleep(3)
        parliamentary_result = None
        while parliamentary_result == None:
            try:
                parliamentary_result = ysk.get_ballot_boxes(ELECTION, ysk_constants.YSKElectionTypes.PARLIAMENTARY, province["id"], district["id"], ysk_constants.YSKIsDomestic.YES, district["electoral_region_id"])
            except Exception as e:
                print_and_log(f"Error while getting parliamentary ballot boxes for {district['name']} with ID {district['id']} in {province['name']} with ID {province['id']}: {e}")
                print_and_log(f"Sleeping for 30 seconds for the next try.")
                time.sleep(30)
        columns_created = []
        for parliamentary_column_name in parliamentary_column_names:
            for ballot_box in parliamentary_result:
                if parliamentary_column_name["column_NAME"] in ballot_box:
                    ballot_box[parliamentary_column_name["ad"]] = ballot_box[parliamentary_column_name["column_NAME"]]
                    del ballot_box[parliamentary_column_name["column_NAME"]]
                    columns_created.append(parliamentary_column_name["ad"])
        for ballot_box in parliamentary_result:
            neighborhood_index = search_in_dict_list(district["neighborhoods"], "id", ballot_box["muhtarlik_ID"])
            # As we already created the neighborhood and ballots above for the presidential election, we don't need to create it again.
            parliamentary_results = district["neighborhoods"][neighborhood_index]["ballot_boxes"][ballot_box["sandik_NO"]]["parliamentary_results"]
            parliamentary_results["total_votes"] = ballot_box["gecerli_OY_TOPLAMI"] + ballot_box["gecersiz_OY_TOPLAMI"]
            parliamentary_results["valid_votes"] = ballot_box["gecerli_OY_TOPLAMI"]
            parliamentary_results["spoilt_votes"] = ballot_box["gecersiz_OY_TOPLAMI"]
            for column_created in columns_created:
                parliamentary_results["numbers"][column_created] = ballot_box[column_created]
                if parliamentary_results["valid_votes"] > 0:
                    parliamentary_results["percentages"][column_created] = round((ballot_box[column_created] / parliamentary_results["valid_votes"])*100, 4)
        print_and_log(f"Added {len(parliamentary_result)} parliamentary ballot boxes to the list of ballot boxes in {district['name']} with ID {district['id']} in {province['name']} with ID {province['id']} (district {district_index + 1}/{len(province['districts'])}, province {province_index + 1}/{len(provinces)})")
        print_and_log(f"Sleeping for 3 seconds to avoid rate limiting.")
        time.sleep(3)
    with open(f"results.json", "w", encoding="utf-8") as f:
        json.dump(provinces, f, ensure_ascii=False, indent=4)
    print_and_log(f"Saved results to results.json")