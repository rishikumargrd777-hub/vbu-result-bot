import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

RESULT_URL = "https://www.vbu.ac.in/notice/result"


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False
        },
        timeout=30
    )


def check_result():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        RESULT_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    found = []

    for a in soup.find_all("a"):
        title = a.get_text(" ", strip=True)
        link = a.get("href")

        if not title or not link:
            continue

        text = title.lower()

        sem7 = (
            "semester 7" in text
            or "semester-7" in text
            or "semester vii" in text
            or "semester-vii" in text
            or "sem 7" in text
            or "sem-7" in text
            or "sem vii" in text
            or "sem-vii" in text
        )

        result = (
            "result" in text
            or "results" in text
        )

        if sem7 and result:

            if link.startswith("/"):
                link = "https://www.vbu.ac.in" + link

            elif not link.startswith("http"):
                link = "https://www.vbu.ac.in/" + link.lstrip("/")

            found.append((title, link))

    return found


if __name__ == "__main__":

    results = check_result()

    if results:

        for title, link in results:

            message = (
                "🚨 VBU SEMESTER 7 RESULT UPDATE 🚨\n\n"
                f"📢 {title}\n\n"
                "🎓 Vinoba Bhave University, Hazaribagh\n\n"
                "🔗 Official Result Link:\n"
                f"{link}"
            )

            send_message(message)

    else:

        print("Semester 7 result not found yet.")
