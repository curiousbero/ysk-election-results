import datetime
import api_caller
import ysk_constants
def print_and_log(message):
    # Get current time and format it as DD/MM/YYYY HH:MM:SS
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = f"{now} -- {message}"
    print(msg)
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(msg + "\n")

def search_in_dict_list(dict_list, key, value):
    for index, dict in enumerate(dict_list):
        if dict[key] == value:
            return index
    return -1

ysk = api_caller.YSKApiCaller()
ELECTION = ysk_constants.YSKElections.GENERAL_2018