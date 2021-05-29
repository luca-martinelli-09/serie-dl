import re
import json


class AnimeSaturnParser:
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
        return driver.find_element_by_css_selector(
            ".anime-title-as .box-trasparente-alternativo").text

    def parse_seasons(self, driver):
        return [{"num": 1}]

    # element is season element got by parse_seasons
    def parse_episodes(self, driver, element):
        episodes = []
        i = 1
        for episode_el in driver.find_elements_by_css_selector(".episodes-button a"):
            episodes.append({"season": element["num"], "episode": i, "title": episode_el.get_attribute(
                "textContent"), "href": episode_el.get_attribute('href')})
            i += 1
        return episodes

    # element is season element got by parse_episodes
    def parse_episode_title(self, driver, element):
        return element["title"].strip()

    # element is season element got by parse_episodes
    def parse_episode_link(self, driver, element):
        return element["href"]

    # element is season element got by parse_episodes
    def parse_ep_ss_num(self, driver, element):
        season_num = element["season"]
        episode = element["episode"]
        return [season_num, episode]

    def parse_dwn_url(self, driver):
        dw_btn = driver.find_element_by_css_selector(".card-body a")
        return dw_btn.get_attribute('href')
