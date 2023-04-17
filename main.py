from dotenv import load_dotenv, dotenv_values
from requests import PreparedRequest, get, post
from datetime import datetime, timedelta
from weekly_tasks import WEEKLY_TASKS

load_dotenv()

config = dotenv_values(".env")
ACCESS_TOKEN = config.get("ACCESS_TOKEN")
HARVEST_ACCOUNT_ID = config.get("HARVEST_ACCOUNT_ID")

TIME_ENTRIES_URL = "https://api.harvestapp.com/v2/time_entries"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Harvest-Account-Id": HARVEST_ACCOUNT_ID,
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def get_time_entries():
    res = get(url=TIME_ENTRIES_URL, headers=HEADERS)

    if not res.ok:
        print("Error: ", res.text)
    else:
        results = res.json()
        return results


def create_time_entry(params):
    req = PreparedRequest()
    req.prepare_url(TIME_ENTRIES_URL, params)
    res = post(url=req.url, headers=HEADERS)

    if not res.ok:
        print("Error: ", res.text)
    else:
        results = res.json()
        return results


def create_recurring_tasks():
    # now = datetime.now()
    now = datetime.strptime("2023-04-14", '%Y-%M-%d')
    monday = now - timedelta(days=now.weekday())
    date = monday

    for tasks in WEEKLY_TASKS:
        spent_date = date.strftime("%Y-%m-%d")
        for t in tasks:
            t["spent_date"] = spent_date
            t["notes"] = "\n".join(t["notes"])
            create_time_entry(t)
        date = date + timedelta(days=1)


create_recurring_tasks()
