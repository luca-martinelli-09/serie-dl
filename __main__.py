from content_parser import ContentParser
from content_downloader import ContentDownloader
import configparser
import argparse
import json
import csv

args_parser = argparse.ArgumentParser(
    description="Download multiple files (serie's episodes or movies) using youtube-dl")
args_parser.add_argument("-i", "--input", dest="sourcefile",
                         help="Input CSV format file with infos about series and movies to download")
args_parser.add_argument("-o", "--output", dest="outputfolder",
                         help="Folder where to download files")
args_parser.add_argument("-d", "--download", dest="parsedfile",
                         help="Input JSON format file with download urls and series/movies infos")
args_parser.add_argument("-p", "--parse", dest="onlyparse", action="store_true",
                         help="Parse movies and series but don't download it")
args_parser.set_defaults(onlyparse=False)
args_parser.add_argument("-c", "--conf", dest="configname",
                         help="Custom config file")
args_parser.set_defaults(configname="default.ini")

args = args_parser.parse_args()


def get_input_contents():
    content_to_parse = []
    insert_one = True

    while insert_one:
        new_insert = {}
        c_type = "movie" if input(
            "Do you want to download a movie or serie? (m/s) ").lower() == "m" else "serie"
        new_insert["type"] = c_type

        c_title = input(
            "Insert title of the content (or enter to get it automatically): ")
        if c_title.strip() != "":
            new_insert["title"] = c_title

        c_url = ""
        while c_url.strip() == "":
            c_url = input("Insert url of content: ").strip()
        new_insert["url"] = c_url

        if c_type == "serie":
            c_seasons = [int(i) for i in input(
                "Insert seasons (divided by space) to download (enter for all): ").split(" ")]
            new_insert["seasons"] = c_seasons

        content_to_parse.append(new_insert)

        insert_one = False if input(
            "Do you want to insert another content? (y/n) ").lower() == "n" else True
        print()

    return content_to_parse


def parse_csv():
    content_to_parse = []
    try:
        with open(args.sourcefile, "r") as f:
            csv_reader = csv.reader(f, delimiter=',')
            header = True
            for row in csv_reader:
                if row[0] != "url":
                    header = False
                if header == False:
                    seasons = []
                    for i in row[3].split(" "):
                        try:
                            seasons.append(int(i))
                        except Exception:
                            pass
                    content_to_parse.append({
                        "url": row[0],
                        "title": row[1].strip() if row[1].strip() != "" else None,
                        "type": row[2],
                        "seasons": seasons
                    })
    except FileNotFoundError as e:
        print("[ERROR]", e)

    return content_to_parse


def get_configs():
    global args
    config = configparser.ConfigParser()
    config.read(args.configname)

    view_log = config["DEFAULT"].getboolean("view_log", True)
    chrome_location = config["PARSER"].get("chrome_location", None)
    chromedriver_location = config["PARSER"].get(
        "chromedriver_location", "./chromedriver/chromedriver.exe")
    headless = config["PARSER"].getboolean("headless", True)
    elapse_time = config["PARSER"].getint("elapse_time", 60)
    file_format = config["DOWNLOADER"].get("file_format", "mp4")
    serie_tmpl = config["DOWNLOADER"].get(
        "serie_tmpl", "{serie_name} - S{season_num:02d}E{episode_num:02d} - {episode_title}")
    movie_tmpl = config["DOWNLOADER"].get("movie_tmpl", "{movie_title}")
    download_folder = config["DOWNLOADER"].get("download_folder", "./")

    parser_options = {
        "view_log": view_log,
        "chrome_location": chrome_location,
        "chromedriver_location": chromedriver_location,
        "headless": headless,
        "elapse_time": elapse_time,
    }

    downloader_options = {
        "view_log": view_log,
        "file_format": file_format,
        "serie_tmpl": serie_tmpl,
        "movie_tmpl": movie_tmpl,
        "download_folder": download_folder,
    }

    return parser_options, downloader_options


if __name__ == "__main__":
    parser_options, downloader_options = get_configs()

    if args.outputfolder is not None:
        downloader_options["downloader_folder"] = args.outputfolder

    contents_parsed = None
    if args.parsedfile is not None:
        try:
            with open(args.parsedfile, "r") as f:
                contents_parsed = json.load(f)
        except Exception as e:
            print("[WARNING]", e)

    if contents_parsed is None:
        content_parser = ContentParser(options=parser_options)

        content_to_parse = []
        if args.sourcefile is None:
            content_to_parse = get_input_contents()
        else:
            content_to_parse = parse_csv()

        contents_parsed = content_parser.parse_contents(content_to_parse)

    if not args.onlyparse:
        downloader = ContentDownloader(options=downloader_options)
        download_success, download_failed = downloader.download_contents(
            contents_parsed)

        print("\n[DOWNLOADED] Successfull downloads:", len(download_success))
        print("[FAILED] Failed downloads (see log.txt):", len(download_failed))

        with open("log.txt", "a+") as f:
            for failed in download_failed:
                if failed["type"] == "movie":
                    f.write(downloader_options["movie_tmpl"].format(
                        movie_title=failed["title"]))
                else:
                    f.write(downloader_options["serie_tmpl"].format(serie_name=failed["serie_title"],
                                                                    season_num=failed["season"],
                                                                    episode_num=failed["episode"],
                                                                    episode_title=failed["title"]))

    else:
        with open('parsed_data.json', 'w') as f:
            json.dump(contents_parsed, f)
            print("\n[SUCCESS] Parsed data saved in parsed_data.json")
