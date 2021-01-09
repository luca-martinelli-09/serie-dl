from __future__ import unicode_literals
from argparse import ArgumentError
import youtube_dl
import json
import os

'''

serie:
    |- title: serie title
    |- url: serie url page
    |- type: "serie"
    |- seasons
        |- season: season number
        |- episodes
            |- episode: episode number
            |- title: episode title
            |- url: episode url page
            |- download_url: download link for youtube_dl

film:
    |- title: film title
    |- url: film url page
    |- type: "film"
    |- download_url: download link for youtube_dl


'''


class ContentDownloader:
    __options = {"file_format": "mp4",
                 "serie_tmpl": "{serie_name} - S{season_num:02d}E{episode_num:02d} - {episode_title}",
                 "film_tmpl": "{film_title}",
                 "download_folder": "./",
                 "view_log": True}
    __download_failed = []
    __download_success = []

    def __init__(self, options):
        self.__options.update(options)
        self.__options["download_folder"] = self.__options["download_folder"].replace(
            "\"", "/").replace("\\", "/")
        self.__options["download_folder"] = self.__options["download_folder"] + \
            "/" if not self.__options["download_folder"].endswith(
                "/") else self.__options["download_folder"]

    def set_options(self, options):
        self.__options.update(options)

    def download_contents(self, contents=None, filename=None):
        if filename is None and contents is None:
            raise ArgumentError(
                "At least one of contents and filename must not be None")
        try:
            if filename is not None and contents is None:
                contents = self.__get_contents_from_file(filename)

            for content in contents:
                if content["type"] == "film":
                    if self.__options["view_log"] is True:
                        print("# Downloading " + content["title"])
                    self.__download_content(content)
                    self.__download_success.append(content)
                else:
                    for season in content["seasons"]:
                        season = content["seasons"][season]
                        for episode in season["episodes"]:
                            serie_info = {
                                "title": content["title"], "season": season["season"]}
                            if self.__options["view_log"] is True:
                                print(
                                    "# Downloading {serie_title}, S{season_num:02d}E{episode_num:02d}: {episode_title}".format(
                                        serie_title=content["title"],
                                        season_num=season["season"],
                                        episode_num=episode["episode"],
                                        episode_title=episode["title"]
                                    ))
                            self.__download_content(episode, serie_info)
                            ep_content_success = episode.copy()
                            ep_content_success["serie_title"] = content["title"]
                            ep_content_success["season"] = season["season"]
                            self.__download_success.append(ep_content_success)
            return self.__download_success, self.__download_failed

        except Exception as e:
            if self.__options["view_log"] is True:
                print("[ERROR] " + e.args[0])

    def __get_contents_from_file(self, filename):
        try:
            with open(filename) as f:
                contents = json.load(f)
                return contents
        except Exception as e:
            raise e

    def __download_content(self, content, serie_info=None):
        if content["download_url"] != "":

            if serie_info is None:
                download_title = self.__options["film_tmpl"].format(
                    film_title=content["title"]
                )
                download_folder = self.__options["download_folder"]
            else:
                download_title = self.__options["serie_tmpl"].format(
                    serie_name=serie_info["title"],
                    season_num=serie_info["season"],
                    episode_num=content["episode"],
                    episode_title=content["title"],
                )
                download_folder = self.__get_download_folder(serie_info)

            ydl_opts = {"outtmpl": download_folder +
                        download_title + "." + self.__options["file_format"],
                        "ignoreerrors": True,
                        "debug_printtraffic": False,
                        "external_downloader_args": ['-loglevel', 'panic']}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([content["download_url"]])
                except:
                    self.__download_failed.append(content)
                    raise("Cannot download file. Skipping download")
        else:
            self.__download_failed.append(content)
            raise Exception("URL doesn't exist. Skippikg download")

    def __get_download_folder(self, serie_info):
        download_folder = self.__options["download_folder"]
        # Create serie folder
        try:
            download_folder += "{serie_title}/".format(
                serie_title=serie_info["title"])
            if not os.path.exists(download_folder):
                os.mkdir(download_folder)
        except KeyError:
            pass

        # Create season folder
        try:
            download_folder += "S{season_num:02d}/".format(
                season_num=serie_info["season"])
            if not os.path.exists(download_folder):
                os.mkdir(download_folder)
        except KeyError:
            pass

        return download_folder
