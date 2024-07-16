from driver import initialise_driver, scrape_url, get_dates_available
from writer import write_subject, write_body

URL_8P_LUXE = (
    r"https://www.landal.nl/parken/strand-resort-ouddorp-duin/accommodaties/8l"
)

def handler(event, context):
    
    driver = initialise_driver()
    soup = scrape_url(driver, URL_8P_LUXE)
    dates = get_dates_available(soup)

    subject = write_subject(dates)
    body = write_body(dates)
    return f'{subject} ----- {body}'

if __name__ == "__main__":
    handler(None, None)