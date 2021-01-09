import json
import time


class GenioParser:
    __options = {"elapse_tile": 30}

    def __init__(self, options):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)

    def parse_title(element):
        return element.find_element_by_css_selector(".data h1").get_attribute('textContent').strip()

    def parse_movie_title(element):
        return element.find_element_by_css_selector(".data h1").get_attribute('textContent').strip()

    def parse_seasons(element):
        return element.find_elements_by_css_selector("#seasons .se-c")

    def parse_episodes(element):
        return element.find_elements_by_css_selector(".episodios li")

    def parse_episode_title(element):
        return element.find_element_by_css_selector(".episodiotitle a").get_attribute('textContent').strip()

    def parse_episode_link(element):
        return element.find_element_by_css_selector(".episodiotitle a").get_attribute('href')

    def parse_ep_ss_num(element):
        # infos in the form "SN - EN"
        return element.find_element_by_class_name("numerando").get_attribute('textContent').split(" - ")

    def parse_dwn_url(self, driver):
        # get video iframe url
        video_frame = driver.find_element_by_css_selector(
            ".play-box-iframe iframe")
        frame_url = video_frame.get_attribute("src")

        # navigate to video frame and initialize video download url
        driver.get(frame_url)
        video_dwl_url = None

        try:
            # if md core is used, get video url
            check_md_core = driver.execute_script("return MDCore")
            return check_md_core["wurl"]
        except:
            pass

        # get current time (if no responses after elapsed_time, exit and return None)
        start_time = time.time()
        elapsed_time = 0  # no time elapsed

        # while no video found or elapsed time not passed, try to get download link from network flow
        while video_dwl_url is None and elapsed_time <= self.__options["elapse_time"]:
            # get network flow
            browser_log = driver.get_log('performance')
            events = []
            for entry in browser_log:
                events.append(json.loads(entry['message'])['message'])

            # check each network request, if contains master.m3u8, it is the download link
            for e in events:
                try:
                    if e['params']['response']["url"].find("master.m3u8") >= 0:
                        video_dwl_url = e['params']['response']["url"]
                except KeyError:
                    pass
            #update elapsed time
            elapsed_time = time.time() - start_time

        # if video download got, then return it, otherwise return exception
        if video_dwl_url is not None:
            return video_dwl_url
        else:
            raise Exception("Error on getting download link")

    def parse_dwl_url_movie(self, driver):
        # same as serie's episodes
        return self.parse_dwn_url(driver)
