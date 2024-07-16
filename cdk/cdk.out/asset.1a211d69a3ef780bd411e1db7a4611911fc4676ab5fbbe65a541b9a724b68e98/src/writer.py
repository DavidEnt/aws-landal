
from datetime import datetime, timedelta

DATE_NEXT_WEEK = datetime.today().date() + timedelta(days=7)

SUBJECT_WEL = "Landal huisje beschikbaar - Mailing Landal Scraper"
SUBJECT_NIET = "Geen Landal huisje beschikbaar - Mailing Landal Scraper"

BODY_HEAD = "Hey,"
BODY_NEXT_WEEK_WEL = "Aankomende week is een Landal huisje te boeken op:\n"
BODY_NEXT_WEEK_NIET = (
    "Aankomende week is er helaas geen Landal huisje beschikbaar om te boeken.\n"
)
BODY_FUTURE_WEEKS = (
    "Toekomstige momenten waarop nu nog Landal huisje beschikbaar zijn:\n"
)
BODY_TAIL = "Good luck!\n\nAutomatic Landal Scraper"

def is_available(dates) -> bool:
    return any([date < DATE_NEXT_WEEK for date in dates])

def write_subject(dates) -> str:
        return SUBJECT_WEL if is_available(dates) else SUBJECT_NIET

def write_body(dates) -> str:
    body = BODY_HEAD + "\n\n"
    
    text = BODY_NEXT_WEEK_WEL if is_available(dates) else BODY_NEXT_WEEK_NIET
    for date in dates:
        if date <= DATE_NEXT_WEEK:
            text += f'- {date.strftime("%A")} {date.strftime("%B %d")}\n'
    body += text + "\n"

    text = "Toekomstige momenten waarop nu nog Landal huisje beschikbaar zijn:\n"
    for date in dates:
        if date > DATE_NEXT_WEEK:
            text += f'- {date.strftime("%A")} {date.strftime("%B %d")}\n'
    body += text + "\n"

    body += BODY_TAIL
    return body
