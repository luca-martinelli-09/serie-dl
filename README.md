# serie_dl

A series and movies downloader for python

## Requirements

Libraries required are **youtube_dl** and **selenium**.

```bash
pip install youtube_dl, selenium
```

You need also **Google Chrome**. If the script return a "Binary Chrome not found" error you must change in **default.ini** the Chrome's binary exe's path.

## Usage

```bash
python serie-dl.py [arguments]
```

Arguments are listed below.

## How it works

You can pass a CSV file or insert data by input.

**Data to insert are:**

- url of the movie/serie page
- title of the movie or the serie (optional, if none this info will be parsed automatically)
- type (movie/serie)
- seasons to download

See [example.csv](example.csv) for an example of CSV file.

**Currently supported these sites:**

- [x] ilgeniodellostreaming
- [x] guardaserie
- [ ] vvvvid
- [ ] seriehd

## Arguments avaiable

You can pass these arguments:

- **-i** or **--input**: Input CSV format file with infos about series and movies to download
- **-o** or **--output**: Folder where to download files
- **-d** or **--download**: Input JSON format file with download urls and series/movies infos
- **-p** or **--parse**: Parse movies and series but don't download it
- **-c** or **--conf**: Use custom config file

## Download from already parsed data

You can pass a JSON file for download file directly from already parsed data. Use **-d** or **--download** argument to pass the JSON file path. It is **very important** to follow the scheme below.

### JSON parsed data structure

The JSON must contain a list of contents.

If content is a movie, the structure must be:

```json
{
  "title": "movie's title",
  "url": "movie's url page",
  "type": "movie",
  "download_url": "download link for youtube_dl"
}
```

If content is a serie, the structure must be:

```json
{
  "title": "series's title",
  "url": "series's url page",
  "type": "serie",
  "seasons": {
    "1": {
      "season": 1,
      "episodes": [
        {
          "episode": 1,
          "title": "episode's title",
          "url": "episodes's url page",
          "download_url": "download link for youtube_dl"
        }
      ]
    }
  }
}
```

See [parsed_data.json](parsed_data.json) for an example.

## Custom config

You can edit [default.ini](default.ini) to change default options used by serie-dl, or you can pass a custom config file with argument **-c** or **--conf**. Settings you can pass are:

```ini
[DEFAULT]
view_log = print logs (yes or not)

[PARSER]
chrome_location = chrome binary location (if different by the default one)
chromedriver_location = chrome driver location
headless = hide browser while getting infos (yes or not)
elapse_time = time after stop looking for download link (time in seconds)

[DOWNLOADER]
file_format = file format
serie_tmpl = downloaded file name format for serie`s episodes
movie_tmpl = downloaded file name format for movies
download_folder = download folder
```

### Serie and Movie file name template

For **serie_tmpl** you can use these variables:

- serie_name
- season_num
- episode_num
- episode_title

For **movie_tmpl** you can use these variables:

- movie_title

**HOW?**

Strings given will be formatted. Example:

`{serie_name} - S{season_num:02d}E{episode_num:02d} - {episode_title}`

will return:

`Black Mirror - S01E02 - Fifteen Million Merits`

## Custom parser

You can also edit the code to add custom parser, following these scheme:

```python
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
```

You can find the file in [serie_dl/parsers/custom_parser.py](serie_dl/parsers/custom_parser.py).

And then:

```python
options = {} # custom options
custom_parser = {"website": CustomParser(options)}
ContentParser(custom_parser=custom_parser)
```
