import requests
import json
import os
import sys
import time
import datetime
import dataclasses
import ysk_constants

class YSKApiCaller:

    def __init__(self):
        self.MAIN_API = "https://acikveri.ysk.gov.tr/api/"

    def get_province_list(self, election_id, election_type_id):
        path = self.MAIN_API + f"getIlList?secimId={election_id}&secimTuru={election_type_id}"
        response = requests.get(path).json()
        return response

    def get_district_list(self, province_id, election_id, election_type_id, region_id_parliament=0):
        path = self.MAIN_API + f"getIlceListWithSecim?secimId={election_id}&ilId={province_id}&secimTuru={election_type_id}&secimCevresiId={region_id_parliament}&sandikTuru=0&yurtIcıDisi=1"
        response = requests.get(path).json()
        return response

    def get_ballot_boxes(self, election_id, election_type_id, province_id, district_id, is_domestic, region_id_parliament=0):
        path = self.MAIN_API + f"getSecimSandikSonucList?secimId={election_id}&secimTuru={election_type_id}&ilId={province_id}&ilceId={district_id}&beldeId=0&birimId=&muhtarlikId=&cezaeviId=&sandikTuru=&sandikNoIlk=&sandikNoSon=&ulkeId=&disTemsilcilikId=&gumrukId=&yurtIciDisi={is_domestic}&sandikRumuzIlk=&sandikRumuzSon=&secimCevresiId={region_id_parliament}&sandikId=&sorguTuru="
        response = requests.get(path).json()
        return response
    
    def get_columns(self, election_id, election_type_id, is_domestic):
        path = self.MAIN_API + f"getSandikSecimSonucBaslikList?secimId={election_id}&secimCevresiId=&ilId=&bagimsiz=1&secimTuru={election_type_id}&yurtIciDisi={is_domestic}"
        response = requests.get(path).json()
        return response
    
    
    

    
