from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urlparse
from serie_dl.parsers.genio_parser import GenioParser


class ContentParser:
    # default options (chrome_location: None get chrome binary automatically)
    __options = {"chrome_location": None,
                 "chromedriver_location": "./chromedriver/chromedriver.exe",
                 "headless": True,
                 "elapse_time": 30,
                 "view_log": True}
    __driver = None
    __contents_got = []
    __site_parsers = {}

    def __init__(self, options, custom_parser=None):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)
        # parser avaiable (user can pass its parser, see README.md for details)
        self.__site_parsers = {
            "ilgeniodellostreaming": GenioParser(self.__options)}
        if custom_parser is not None:
            self.__site_parsers.update(custom_parser)

    def set_options(self, options):
        # update options
        self.__options.update(options)

    def parse_contents(self, contents):
        # setup chrome driver
        self.__setup_driver()

        # get main infos for each content (title, number of seasons, etc...)
        for content in contents:
            if "type" in content.keys() and content["type"] == "movie":
                movie_info = self.__get_movie_info(content)
                # if movie infos got append to contents
                # movie info get also download link for youtube-dl
                if movie_info is not None:
                    self.__contents_got.append(movie_info)
            else:
                serie_info = self.__get_serie_info(content)
                # if serie infos got append to contents
                if serie_info is not None:
                    self.__contents_got.append(serie_info)

        if self.__options["view_log"] is True:
            print("\nGetting download links for episodes\n")

        # start get download links for youtube-dl
        for serie in self.__contents_got:
            if serie is not None and serie["type"] == "serie":
                for season in serie["seasons"]:
                    season = serie["seasons"][season]
                    for episode in season["episodes"]:
                        # navigate in episode page
                        self.__driver.get(episode["url"])

                        if self.__options["view_log"] is True:
                            print("Getting download url for {serie_title}, S{season_num:02d}E{episode_num:02d}: {episode_title}".format(
                                serie_title=serie["title"],
                                season_num=season["season"],
                                episode_num=episode["episode"],
                                episode_title=episode["title"]))

                        try:
                            # get parser and get episode download link for youtube-dl
                            parse_info = self.__get_parse_info(serie["url"])
                            episode_url_download = parse_info.parse_dwn_url(
                                self.__driver)
                            episode["download_url"] = episode_url_download
                        except Exception as e:
                            if self.__options["view_log"] is True:
                                print("[ERROR]", e)

        # close driver and return contents got
        self.__driver.close()
        return self.__contents_got

    def __get_serie_info(self, serie):
        try:
            serie_url = serie["url"]
            # get parser
            parse_info = self.__get_parse_info(serie_url)

            # navigate to serie's page
            self.__driver.get(serie_url)

            # if serie title is given, use it, otherwise get automatically
            serie_title = serie["title"] if "title" in serie.keys(
            ) and serie["title"] is not None else parse_info.parse_title(self.__driver)
            # if seasons to download given, otherwise download all
            seasons_selected = serie["seasons"] if "seasons" in serie.keys(
            ) else None

            # serie main info
            serie_info = {
                "title": serie_title,
                "url": serie_url,
                "type": "serie",
                "seasons": {}
            }

            if self.__options["view_log"] is True:
                seasons_str = ", ".join(
                    str(ss_num) for ss_num in seasons_selected) if seasons_selected is not None else "all"
                print("\n### {serie_title} ###\nSeasons to download: {seasons_str}".format(
                    serie_title=serie_title.upper(), seasons_str=seasons_str))

            # select all seasons
            for season in parse_info.parse_seasons(self.__driver):
                # select episodes for season
                for episode in parse_info.parse_episodes(season):
                    # parse episode title, link, season number and episode number
                    episode_title = parse_info.parse_episode_title(episode)
                    episode_link = parse_info.parse_episode_link(episode)
                    season_num, episode_num = parse_info.parse_ep_ss_num(
                        episode)
                    season_num, episode_num = int(season_num), int(episode_num)

                    # if season is selected by the user add it to serie_info
                    if seasons_selected is None or season_num in seasons_selected:
                        if season_num not in serie_info["seasons"]:
                            serie_info["seasons"][season_num] = {
                                "season": season_num, "episodes": []}

                        serie_info["seasons"][season_num]["episodes"].append({
                            "episode": episode_num,
                            "title": episode_title,
                            "url": episode_link,
                            "download_url": None
                        })

            if self.__options["view_log"] is True:
                # count episodes and seasons got
                seasons_got = len(serie_info["seasons"])
                episodes_got = 0
                for seas in serie_info["seasons"]:
                    season = serie_info["seasons"][seas]
                    episodes_got += len(season["episodes"])
                print("\tFound {num_seasons} seasons and {num_episodes} episodes... ".format(
                    num_seasons=seasons_got,
                    num_episodes=episodes_got))

            return serie_info

        except Exception as e:
            if self.__options["view_log"] is True:
                print("[ERROR]", e)
        return None

    def __get_movie_info(self, movie):
        try:
            movie_url = movie["url"]
            # get parser
            parse_info = self.__get_parse_info(movie_url)

            # navigate to serie's page
            self.__driver.get(movie_url)

            # if movie title is given, use it, otherwise get automatically
            movie_title = movie["title"] if "title" in movie.keys(
            ) and movie["title"] is not None else parse_info.parse_movie_title(self.__driver)

            # movie main info
            movie_info = {
                "title": movie_title,
                "url": movie_url,
                "type": "movie",
                "download_url": None
            }

            if self.__options["view_log"] is True:
                print("\n### {movie_title} ###".format(
                    movie_title=movie_title.upper()))

            # get download link for youtube-dl, None if not found
            movie_info["download_url"] = parse_info.parse_dwl_url_movie(
                self.__driver)

            if self.__options["view_log"] is True:
                if movie_info["download_url"] is not None:
                    print("\tDownload link found")
                else:
                    print("\tDownload link not found")

            return movie_info

        except Exception as e:
            if self.__options["view_log"] is True:
                print("[ERROR]", e)
        return None

    def __get_parse_info(self, serie_url):
        # parse url and check if there is one site in parsers list
        url_info = urlparse(serie_url)
        site_title = url_info.netloc
        for site_key in self.__site_parsers.keys():
            if site_title.lower().find(site_key) >= 0:
                return self.__site_parsers[site_key]
        raise Exception(f"Site {site_title} is not supported")

    def __setup_driver(self):
        # get network flow
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = webdriver.ChromeOptions()
        if self.__options["chrome_location"] is not None:
            chrome_options.binary_location = self.__options["chrome_location"]
        chrome_options.add_argument('--window-size=1080,720')
        # hide browser while getting infos
        if self.__options["headless"] == True:
            chrome_options.add_argument('--headless')
        # hide info and warnings
        chrome_options.add_argument('--log-level=3')
        # set driver
        self.__driver = webdriver.Chrome(executable_path=self.__options["chromedriver_location"],
                                         desired_capabilities=caps, options=chrome_options)
