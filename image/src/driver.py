from datetime import datetime
from tempfile import mkdtemp
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def initialise_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log"
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    return driver

def scrape_url(driver, url):
    """Scrape the URL."""

    driver.get(url)
    time.sleep(3)
    
    # click the cookie banner away
    try:
        shadow_parent = driver.find_element(By.XPATH, r'/html/body/consent-slide-in-component')
        driver.execute_script('return arguments[0].shadowRoot', shadow_parent).find_element(By.CLASS_NAME, r"c-button--important").click()
        time.sleep(1)
    except:
        pass

    # click to the earliest day available.
    while True:
        try:
            driver.find_element(By.CLASS_NAME, "js-finetuner-navigation-previous").click()
            time.sleep(1)
        except:
            break 

    time.sleep(1)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    
    return soup

def get_dates_available(soup):
    """Get list of available dates from the beautiful soup."""
    # find all date elements
    elems = soup.find_all("div", class_="c-finetuner__content js-finetuner-content")
    elems_selected = elems[0].find_all(
        "td", class_="js-finetuner-table-cell c-finetuner__table-cell is-selected"
    )
    elems_not_selected = elems[0].find_all(
        "td", class_="js-finetuner-table-cell c-finetuner__table-cell"
    )
    elems_filled = elems_selected + elems_not_selected

    # extract dates from date elements and set in standard time format
    dates = [elem["data-arrival-date"] for elem in elems_filled]
    dates = [datetime.strptime(date, "%d-%m-%Y").date() for date in dates]
    dates.sort()

    return dates