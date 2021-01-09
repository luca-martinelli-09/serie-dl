import json
import time


class VVVVIDParser:
    __options = {}

    def __init__(self, options):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)

    def parse_title(self, element):
        pass

    def parse_movie_title(self, element):
        pass

    def parse_seasons(self, element):
        pass

    def parse_episodes(self, element):
        pass

    def parse_episode_title(self, element):
        pass

    def parse_episode_link(self, element):
        pass

    def parse_ep_ss_num(self, element):
        # infos in the form "SN - EN"
        pass

    def parse_dwn_url(self, driver):
        # get video iframe url
        pass

    def parse_dwl_url_movie(self, driver):
        # same as serie's episodes
        pass
