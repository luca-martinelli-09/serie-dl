import json
import time


class GenioParser:
    __options = {"elapse_tile": 60}

    def __init__(self, options):
        self.__options.update(options)

    def parse_title(self, element):
        return element.find_element_by_css_selector(".data h1").get_attribute('textContent').strip()
    
    def parse_film_title(self, element):
        return element.find_element_by_css_selector(".data h1").get_attribute('textContent').strip()

    def parse_seasons(self, element):
        return element.find_elements_by_css_selector("#seasons .se-c")

    def parse_episodes(self, element):
        return element.find_elements_by_css_selector(".episodios li")

    def parse_episode_title(self, element):
        return element.find_element_by_css_selector(".episodiotitle a").get_attribute('textContent').strip()

    def parse_episode_link(self, element):
        return element.find_element_by_css_selector(".episodiotitle a").get_attribute('href')

    def parse_ep_ss_num(self, element):
        return element.find_element_by_class_name("numerando").get_attribute('textContent').split(" - ")

    def parse_dwn_url(self, driver):
        video_frame = driver.find_element_by_css_selector(
            ".play-box-iframe iframe")
        frame_url = video_frame.get_attribute("src")

        driver.get(frame_url)
        video_dwl_url = None
        
        try:
            check_md_core = driver.execute_script("return MDCore")
            return check_md_core["wurl"]
        except:
            pass

        start_time = time.time()
        elapsed_time = 0
        while video_dwl_url is None and elapsed_time <= self.__options["elapse_time"]:
            browser_log = driver.get_log('performance')
            events = []
            for entry in browser_log:
                events.append(json.loads(entry['message'])['message'])

            for e in events:
                try:
                    if e['params']['response']["url"].find("master.m3u8") >= 0:
                        video_dwl_url = e['params']['response']["url"]
                except KeyError:
                    pass
            elapsed_time = time.time() - start_time

        if video_dwl_url is not None:
            return video_dwl_url
        else:
            raise Exception("Error on getting download link")
    
    def parse_dwl_url_film(self, driver):
        return self.parse_dwn_url(driver)
