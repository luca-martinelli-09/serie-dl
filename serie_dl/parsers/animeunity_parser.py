import requests
import json
import re

class AnimeUnityParser:
    __options = {}
    __content = {}
    # ["movie"] for movie only, ["serie"] for serie only,
    support = ["serie"]

    def __init__(self, options=None, content=None):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)
        if content is not None:
            self.__content.update(content)

    # called to set content (eg. you can get page url)
    def set_content(self, content):
        self.__content.update(content)

    # driver is selenium webdriver
    def parse_title(self, driver):
        return driver.find_element_by_css_selector("h1.title").get_attribute("textContent").strip()

    def parse_seasons(self, driver):
        response = requests.get(
            "https://lucamartinelli.hopto.org/interface.php?function=serie-dl-animeunity&url=" + self.__content["url"]).text
        data = json.loads(response)
        return [{"episodes": data["episodes"]}]

    # element is season element got by parse_seasons
    def parse_episodes(self, driver, element):
        return element["episodes"]

    # element is episode element got by parse_episodes
    def parse_episode_title(self, driver, element):
        return "Episodio " + element["number"]

    # element is episode element got by parse_episodes
    def parse_episode_link(self, driver, element):
        return element["link"]

    # element is episode element got by parse_episodes
    def parse_ep_ss_num(self, driver, element):
        return [1, int(element["number"])]

    def parse_dwn_url(self, driver):
        return driver.current_url


