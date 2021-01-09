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

movie:
    |- title: movie title
    |- url: movie url page
    |- type: "movie"
    |- download_url: download link for youtube_dl


'''


class ContentDownloader:
    __options = {"file_format": "mp4",
                 "serie_tmpl": "{serie_name} - S{season_num:02d}E{episode_num:02d} - {episode_title}",
                 "movie_tmpl": "{movie_title}",
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
        if filename is not None and contents is None:
            contents = self.__get_contents_from_file(filename)

        for content in contents:
            if content["type"] == "movie":
                if self.__options["view_log"] is True:
                    print("[DOWNLOADING] {title}".format(
                        title=content["title"]))
                try:
                    self.__download_content(content)
                    self.__download_success.append(content)
                except DownloadException as e:
                    self.__download_failed.append(content)
                    if self.__options["view_log"] is True:
                        print("\t[ERROR]", e)
            else:
                for season in content["seasons"]:
                    season = content["seasons"][season]
                    for episode in season["episodes"]:
                        if self.__options["view_log"] is True:
                            print(
                                "[DOWNLOADING] {serie_title}, S{season_num:02d}E{episode_num:02d}: {episode_title}".format(
                                    serie_title=content["title"],
                                    season_num=season["season"],
                                    episode_num=episode["episode"],
                                    episode_title=episode["title"]
                                ))
                        ep_content = episode.copy()
                        ep_content["serie_title"] = content["title"]
                        ep_content["season"] = season["season"]
                        try:
                            self.__download_content(ep_content)
                            self.__download_success.append(ep_content)
                        except DownloadException as e:
                            self.__download_failed.append(ep_content)
                            if self.__options["view_log"] is True:
                                print("\t[ERROR]", e)

        return self.__download_success, self.__download_failed

    def __get_contents_from_file(filename):
        try:
            with open(filename) as f:
                contents = json.load(f)
                return contents
        except Exception:
            return []

    def __download_content(self, content):
        if content["download_url"] != "":
            if "serie_title" not in content.keys():
                download_title = self.__options["movie_tmpl"].format(
                    movie_title=content["title"]
                )
                download_folder = self.__options["download_folder"]
            else:
                download_title = self.__options["serie_tmpl"].format(
                    serie_name=content["serie_title"],
                    season_num=content["season"],
                    episode_num=content["episode"],
                    episode_title=content["title"],
                )
                download_folder = self.__get_download_folder(content)

            ydl_opts = {"outtmpl": download_folder +
                        download_title + "." + self.__options["file_format"],
                        "debug_printtraffic": False,
                        "external_downloader_args": ['-loglevel', 'panic']}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([content["download_url"]])
                except:
                    raise DownloadException(
                        "Cannot download file. Skipping download")
        else:
            raise DownloadException("URL doesn't exist. Skippikg download")

    def __get_download_folder(self, serie_info):
        download_folder = self.__options["download_folder"]
        # Create serie folder
        try:
            download_folder += "{serie_title}/".format(
                serie_title=serie_info["serie_title"])
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


class DownloadException(Exception):
    def __init__(self, message="Cannot download file. Skipping download"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
