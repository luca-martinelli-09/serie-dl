import json
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class MoodleUniPDParser:
    __options = {}
    __content = {}
    # ["movie"] for movie only, ["serie"] for serie only,
    support = ["serie", "movie"]
    __logged = False

    def __init__(self, options=None, content=None):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)
        if content is not None:
            self.__content.update(content)
    
    def __wait_login(self):
        if self.__logged:
            return True
        logged = input("Press y when you're logged in: ")
        while logged != "y":
            logged = input("Press y when you're logged in: ")
        if logged == "y":
            self.__logged = True
            return True

    # called to set content (eg. you can get page url)
    def set_content(self, content):
        self.__content.update(content)

    # driver is selenium webdriver
    def parse_title(self, driver):
        if self.__wait_login():
            return driver.find_element_by_css_selector(".heading-title").get_attribute("textContent").strip()

    def parse_movie_title(self, driver):
        if self.__wait_login():
            return self.parse_title(driver)

    def parse_seasons(self, driver):
        if self.__wait_login():
            return [driver.find_element_by_css_selector(".course-content")]

    # element is season element got by parse_seasons
    def parse_episodes(self, driver, element):
        ret_elements = []
        i = 1
        for episode_element in element.find_elements_by_css_selector(".modtype_kalvidres"):
            ret_elements.append({
                "season": 1,
                "episode": i,
                "element": episode_element
            })
            i += 1
        return ret_elements

    # element is episode element got by parse_episodes
    def parse_episode_title(self, driver, element):
        element_ep = element["element"]
        return element_ep.find_element_by_css_selector(".instancename").text

    # element is episode element got by parse_episodes
    def parse_episode_link(self, driver, element):
        element_ep = element["element"]
        return element_ep.find_element_by_css_selector("a").get_attribute("href")

    # element is episode element got by parse_episodes
    def parse_ep_ss_num(self, driver, element):
        return [element["season"], element["episode"]]

    def parse_dwn_url(self, driver):
        # start video
        wait = WebDriverWait(driver, 10)
        videoplayer = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#contentframe")))
        driver.get(videoplayer.get_attribute("src"))

        player_btn = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#kplayer")))
        player_btn.click()

        # initialize video download url
        video_dwl_url = None

        # get current time (if no responses after elapsed_time, exit and return None)
        start_time = time.time()
        elapsed_time = 0  # no time elapsed

        # while no video found or elapsed time not passed, try to get download link from network flow
        while video_dwl_url is None and elapsed_time <= self.__options["elapse_time"]:
            # get network flow
            browser_log = driver.get_log("performance")
            events = []
            for entry in browser_log:
                events.append(json.loads(entry["message"])["message"])

            # check each network request, if contains master.m3u8, it is the download link
            for e in events:
                try:
                    if e["params"]["response"]["url"].find("index.m3u8") >= 0:
                        video_dwl_url = e["params"]["response"]["url"]
                except KeyError:
                    pass
            # update elapsed time
            elapsed_time = time.time() - start_time

        # if video download got, then return it, otherwise return exception
        if video_dwl_url is not None:
            return video_dwl_url
        else:
            raise Exception("Error on getting download link")
    
    def parse_dwl_url_movie(self, driver):
        if self.__wait_login():
            return self.parse_dwn_url(driver)
