from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

class Driver:
    """Classe pour gérer une instance de WebDriver pour des tâches de scraping."""
    def __init__(self, headless=False, **kwargs):
        self._driver = None
        self.headless = headless
        self.initialize_driver()
        self.configure_driver()

    def __new__(cls, *args, **kwargs):
        """Assure qu'une seule instance de Driver est créée."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Driver, cls).__new__(cls)
        return cls.instance

    def initialize_driver(self):
        """Initialise le WebDriver avec les options nécessaires."""
        # initialisation with selenium.webdriver.Chrome
        if self._driver:
            raise ValueError("WebDriver déjà initialisé.")
        chrome_options = ChromeOptions()
        if self.headless:
            chrome_options.add_argument("--headless=new")  # Utilise le mode headless moderne

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")

        service = ChromeService()

        self._driver = webdriver.Chrome(service=service, options=chrome_options)
        self.configure_driver()

    def configure_driver(self):
        """Configure le WebDriver après son initialisation."""
        if not self._driver:
            raise ValueError("WebDriver non initialisé.")
        self._driver.set_page_load_timeout(60)
        self._driver.maximize_window()

    @property
    def driver(self):
        if not self._driver:
            raise ValueError("WebDriver non initialisé.")
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    def quit(self):
        """Ferme proprement le WebDriver."""
        if self._driver:
            self._driver.quit()
            self._driver = None
