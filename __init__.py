from content_parser import ContentParser
from content_downloader import ContentDownloader
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

content_parser = ContentParser(options={
    "chrome_location": "C:/Program Files (x86)/Google/Chrome Beta/Application/chrome.exe"})

contents = content_parser.parse_contents(
    [{"url": "https://ilgeniodellostreaming.cat/film/007-bersaglio-mobile/", "type": "film"}])

downloader = ContentDownloader({"download_folder": "./downloads"})
download_success, download_failed = downloader.download_contents(contents)

print("\nDOWNLOADED " + str(len(download_success)))
print("\nFAILED " + str(len(download_failed)))

print(download_success)
print(download_failed)
