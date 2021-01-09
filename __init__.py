from content_parser import ContentParser

serie_parser = ContentParser(options={
    "chrome_location": "C:/Program Files (x86)/Google/Chrome Beta/Application/chrome.exe"})

series_got = serie_parser.parse_contents(
    [{"url": "https://ilgeniodellostreaming.cat/serietv/blackaf/"}, {"url": "https://ilgeniodellostreaming.cat/film/escape-from-pretoria-streaming/", "type": "film"}])
print(series_got)
