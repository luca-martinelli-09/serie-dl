from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json


class ContentDownloader:
    __options = {"file_format": "mp4",
                 "file_tmpl": "{serie_name} - S{season_num:02d}E{episode_num:02d} - {episode_title}"}

    def __process_browser_log_entry(entry):
        response = json.loads(entry['message'])['message']
        return response

    def __init__(self, options):
        self.__options.update(options)

    def set_options(self, options):
        self.__options.update(options)
    
    
