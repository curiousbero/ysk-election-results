# ysk-election-results
Python script to download general election results from the Turkish Supreme Electoral Council(YSK - *Yüksek Seçim Kurulu*)

## Using it yourself

1. Download or clone the repository.
2. In `globals.py`, set line 20 - the `ELECTION` constant - to your desired election. The possible options are `GENERAL_2018`(done June 24th 2018) and `GENERAL_2023`(done May 14th 2023).
3. Run `province_downloader.py`. This will download the districts of every Turkish province and which province belongs to which parliamentary electoral region. The end result will be saved to `provinces.json`.
4. Run `result_downloader.py`. This will download the election results(just the raw numbers - not how many MPs got elected etc.) by the each ballot box. The end result will be saved to `results.json`
    * **NOTE: This step will take a long time(about 3-4 hours) given the size of the file, the number of web requests required, and the rate limits of the YSK API. The script may use up to 1 GB of RAM during the download, and the file size of `results.json` may exceed several GBs.**
5. Enjoy!

## Inner workings
The data source for the election results is YSK's Open Data Portal(accessible [here](https://acikveri.ysk.gov.tr/anasayfa)). The Open Data Portal does not have documentation for an API, however the API used under the hood is not hard to reverse-engineer. The core API URL is `https://acikveri.ysk.gov.tr/api/` and the 4 endpoints used in this script are:

### `/getIlList`
Get list of provinces in Turkey.

#### Query parameters
* `secimId` - Election ID.
* `secimTuru` - Election type(8 for parliamentary, 9 for presidential). If the value 8 is passed, then the endpoint returns the list of electoral regions instead of the list of provinces.

### `/getIlceListWithSecim`
TODO

### `/getSecimSandikSonucList`
TODO

### `/getSandikSecimSonucBaslikList`
TODO

## Required packages
1. `requests` - install with `pip install requests` on Windows or `pip3 install requests` on Linux.

## Python version
At least Python 3.8 is required for running this script.

## Known issues
* In `provinces.json`, the name of the provinces, if the province has more than 1 electoral region, is saved as `{PROVINCE}-1`.
