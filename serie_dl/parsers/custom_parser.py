class CustomParser:
    __options = {}

    def __init__(self, options):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)

    # element is selenium webdriver
    def parse_title(self, element):
        # return string of serie's title
        pass

    def parse_movie_title(self, element):
        # return string of movie's title
        pass

    def parse_seasons(self, element):
        # return selenium elements of seasons
        pass

    # element is season element got by parse_seasons
    def parse_episodes(self, element):
        # return selenium elements of episodes
        pass

    def parse_episode_title(self, element):
        # return episode title as string
        pass

    def parse_episode_link(self, element):
        # return episode link page as string
        pass

    def parse_ep_ss_num(self, element):
        # return list of episode number and season number (int)
        pass

    def parse_dwn_url(self, element):
        # return download url as string or None or Exception
        pass

    def parse_dwl_url_movie(self, element):
        # return download url as string or None or Exception
        pass
