import urllib.parse as urlparse
from urllib.parse import parse_qs


class SerieHDParser:
    __options = {}
    __content = {}
    support = ["serie"]

    def __init__(self, options=None, content=None):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)
        if content is not None:
            self.__content.update(content)

    def set_content(self, content):
        self.__content.update(content)

    # driver is selenium webdriver
    def parse_title(self, driver):
        return driver.find_element_by_css_selector("meta[property=\"og:title\"]").get_attribute("content").strip()

    def parse_seasons(self, driver):
        serie_frame = driver.find_element_by_css_selector("#iframeVid")
        driver.get(serie_frame.get_attribute("src"))
        return [element.get_attribute("href") for element in driver.find_elements_by_css_selector("#seasonsModal li a")]

    # element is season element got by parse_seasons
    def parse_episodes(self, driver, element):
        driver.get(element)
        return [{"title": episode_el.get_attribute('textContent'), "href": episode_el.get_attribute('href')} for episode_el in driver.find_elements_by_css_selector("#episodesModal li a")]

    # element is season element got by parse_episodes
    def parse_episode_title(self, driver, element):
        return element["title"].strip()

    # element is season element got by parse_episodes
    def parse_episode_link(self, driver, element):
        return element["href"]

    # element is season element got by parse_episodes
    def parse_ep_ss_num(self, driver, element):
        parsed = urlparse.urlparse(element["href"])
        parse_q = parse_qs(parsed.query)
        return [int(parse_q["season"][0]) + 1, int(parse_q["episode"][0]) + 1]

    def parse_dwn_url(self, driver):
        # return download url as string or None or Exception
        pass
