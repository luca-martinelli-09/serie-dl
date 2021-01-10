class CustomParser:
    __options = {}
    __content = {}
    # ["movie"] for movie only, ["serie"] for serie only,
    support = ["movie", "serie"]

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
        # return string of serie's title
        pass

    def parse_movie_title(self, driver):
        # return string of movie's title
        pass

    def parse_seasons(self, driver):
        # return selenium elements of seasons
        pass

    # element is season element got by parse_seasons
    def parse_episodes(self, driver, element):
        # return selenium elements of episodes
        pass

    # element is episode element got by parse_episodes
    def parse_episode_title(self, driver, element):
        # return episode title as string
        pass

    # element is episode element got by parse_episodes
    def parse_episode_link(self, driver, element):
        # return episode link page as string
        pass

    # element is episode element got by parse_episodes
    def parse_ep_ss_num(self, driver, element):
        # return list of episode number and season number (int)
        pass

    def parse_dwn_url(self, driver):
        # return download url as string or None or Exception
        pass

    def parse_dwl_url_movie(self, driver):
        # return download url as string or None or Exception
        pass
