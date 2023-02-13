import os
import requests
from bs4 import BeautifulSoup
import hashlib
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
        return soup.prettify()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to scrape site ({e})")
        return ""

def check_update(url):
    current_content = scrape_site(url)
    if current_content == "":
        return

    current_hash = hashlib.sha256(current_content.encode()).hexdigest()

    try:
        with open("previous_hash.txt", "r") as f:
            previous_hash = f.read()
    except:
        previous_hash = ""

    if current_hash != previous_hash:
        send_notification("スケジュールが更新されました。")
        with open("previous_hash.txt", "w") as f:
            f.write(current_hash)

if __name__ == "__main__":
    load_dotenv()

    url = os.environ.get("TARGET_URL")
    if url is None:
        print("Error: TARGET_URL not found in environment variables.")

    check_update(url)
