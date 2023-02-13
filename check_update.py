import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def send_notification(message):
    url = "https://notify-api.line.me/api/notify"
    token = os.environ.get("LINE_NOTIFY_ACCESS_TOKEN")
    if token is None:
        print("Error: LINE_NOTIFY_ACCESS_TOKEN not found in environment variables.")
        return

    headers = {"Authorization": "Bearer " + token}
    payload = {"message": message}
    try:
        r = requests.post(url, headers=headers, params=payload)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to send notification ({e})")

def scrape_site(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        for td in soup.find_all('td'):
            if td.get('colspan') == '8':
                return td.text
        return ""
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to scrape site ({e})")
        return ""

def check_update(url):
    current_date = scrape_site(url)
    if current_date == "":
        return

    try:
        with open("previous.txt", "r") as f:
            previous_date = f.read()
    except:
        previous_date = ""

    if current_date != previous_date:
        send_notification('{}'.format(current_date)+'のスケジュールが更新されました。')
        with open("previous.txt", "w") as f:
            f.write(current_date)

if __name__ == "__main__":
    load_dotenv()

    url = os.environ.get("TARGET_URL")
    if url is None:
        print("Error: TARGET_URL not found in environment variables.")

    check_update(url)
