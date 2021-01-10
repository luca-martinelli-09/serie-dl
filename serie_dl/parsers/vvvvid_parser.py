import re
import requests
import json


class VVVVIDParser:
    __options = {}
    __content = {}
    # ["movie"] for movie only, ["serie"] for serie only,
    support = ["movie", "serie"]
    __current_id = None
    __current_conn_id = None
    __current_url = ""

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
        self.__current_url = driver.current_url
        curr_id = re.search(".*/show/([0-9]+)/.*", self.__current_url)
        self.__current_id = int(curr_id.group(1))
        self.__current_conn_id = driver.execute_script("return vvvvid.conn_id")
        info_url = "https://www.vvvvid.it/vvvvid/ondemand/" + \
            str(self.__current_id) + "/info/?conn_id=" + \
            str(self.__current_conn_id)
        driver.get(info_url)
        response = json.loads(
            driver.find_element_by_tag_name("pre").text)
        return response["data"]["title"]

    def parse_movie_title(self, driver):
        return self.parse_title(driver)

    def parse_seasons(self, driver):
        season_url = "https://www.vvvvid.it/vvvvid/ondemand/" + \
            str(self.__current_id) + "/seasons/?conn_id=" + \
            str(self.__current_conn_id)
        driver.get(season_url)
        response = json.loads(
            driver.find_element_by_tag_name("pre").text)
        seasons = []
        for season in response["data"]:
            season_title = season["name"]
            if season_title.lower().find("live") < 0 and season_title.lower().find("extra") < 0:
                search_season_num = re.search(".*([0-9]+)$", season_title)
                season_num = season["number"]
                if search_season_num is not None:
                    season_num = int(search_season_num.group(1))
                seasons.append({"num": season_num, "season": season})
        return seasons

    # element is season element got by parse_seasons
    def parse_episodes(self, driver, element):
        episodes = []
        for episode in element["season"]["episodes"]:
            episodes.append(
                {"season": element["num"], "episode": episode})
        return episodes

    # element is season element got by parse_episodes
    def parse_episode_title(self, driver, element):
        episode = element["episode"]
        return episode["title"]

    # element is season element got by parse_episodes
    def parse_episode_link(self, driver, element):
        episode = element["episode"]
        data_seasonid = episode["season_id"]
        data_id = episode["video_id"]
        data_title = episode["title"]
        data_title = re.sub("[!@#$%^&*(),.?\":{}|<>]", "", data_title)
        data_title = re.sub("['\s]", "-", data_title.strip())
        return "{url}/{season_id}/{episode_id}/{episode_title}".format(url=self.__current_url,
                                                                       season_id=data_seasonid,
                                                                       episode_id=data_id,
                                                                       episode_title=data_title)

    # element is season element got by parse_episodes
    def parse_ep_ss_num(self, driver, element):
        season_num = element["season"]
        episode = element["episode"]
        episode_num = int(episode["number"])
        return [season_num, episode_num]

    def parse_dwn_url(self, driver):
        return driver.current_url

    def parse_dwl_url_movie(self, driver):
        info_url = "https://www.vvvvid.it/vvvvid/ondemand/" + \
            str(self.__current_id) + "/seasons/?conn_id=" + \
            str(self.__current_conn_id)
        driver.get(info_url)
        response = json.loads(
            driver.find_element_by_tag_name("pre").text)
        episode = {"episode": response["data"][0]["episodes"][0]}
        return self.parse_episode_link(driver, episode)
