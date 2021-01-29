from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle


class CookieSaver:
    # default options (chrome_location: None get chrome binary automatically)
    __options = {"chrome_location": None,
                 "chromedriver_location": "./chromedriver/chromedriver.exe",
                 "headless": True,
                 "elapse_time": 30,
                 "view_log": True}
    __driver = None

    def __init__(self, options):
        # update options with one given by the user (if there's)
        if options is not None:
            self.__options.update(options)
        # open browser
        self.__setup_driver()

    def set_options(self, options):
        # update options
        self.__options.update(options)

    def save_cookies(self):
        pickle.dump(self.__driver.get_cookies(), open("cookies.pkl", "wb"))
        self.__driver.quit()

    def __setup_driver(self):
        # get network flow
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = webdriver.ChromeOptions()
        if self.__options["chrome_location"] is not None:
            chrome_options.binary_location = self.__options["chrome_location"]
        chrome_options.add_argument('--window-size=1080,720')
        # hide info and warnings
        chrome_options.add_argument('--log-level=3')
        # set driver
        self.__driver = webdriver.Chrome(executable_path=self.__options["chromedriver_location"],
                                         desired_capabilities=caps, options=chrome_options)
