from dotenv import load_dotenv, dotenv_values
from requests import PreparedRequest, get, post
from datetime import datetime, timedelta

load_dotenv()

config = dotenv_values(".env")
ACCESS_TOKEN = config["ACCESS_TOKEN"]
HARVEST_ACCOUNT_ID = config["HARVEST_ACCOUNT_ID"]

PROJECT_ID = config["PROJECT_ID"]
PROJECT_TASK_ID = config["PROJECT_TASK_ID"]
GM_PROJECT_ID = config["GM_PROJECT_ID"]
GM_MISC_NON_BILLABLE_TASK_ID = config["GM_MISC_NON_BILLABLE_TASK_ID"]
GM_PTO_HOLIDAY_TASK_ID = config["GM_PTO_HOLIDAY_TASK_ID"]

BASE_URL = "https://api.harvestapp.com"
TIME_ENTRIES_URL = f"{BASE_URL}/v2/time_entries"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Harvest-Account-Id": HARVEST_ACCOUNT_ID,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

WEEKLY_PROJECT_TASKS = [
    # MONDAY
    {
        "project_id": PROJECT_ID,
        "task_id": PROJECT_TASK_ID,
        "hours": "8",
        "notes": ["GM Standup", "Internal huddle", "Prod/Eng Sync"],
    },
    # TUESDAY
    {
        "project_id": PROJECT_ID,
        "task_id": PROJECT_TASK_ID,
        "hours": "8",
        "notes": ["Artemis Integration Sync", "Dev Standup"],
    },
    # WEDNESDAY
    {
        "project_id": PROJECT_ID,
        "task_id": PROJECT_TASK_ID,
        "hours": "8",
        "notes": ["Internal huddle", "Leadership Check-In"],
    },
    # THURSDAY
    {
        "project_id": PROJECT_ID,
        "task_id": PROJECT_TASK_ID,
        "hours": "8",
        "notes": ["Tech leads sync", "Dev Standup", "Artemis Integration Sync"],
    },
    # FRIDAY
    {
        "project_id": PROJECT_ID,
        "task_id": PROJECT_TASK_ID,
        "hours": "8",
        "notes": ["GM standup", "Internal huddle", "Project touchbase"],
    },
]


def get_time_entries():
    url = TIME_ENTRIES_URL
    res = get(url=url, headers=HEADERS)

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
        print("results", results)
        return results


def create_reoccurring_tasks():
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    date = monday

    for i in WEEKLY_PROJECT_TASKS:
        i["spent_date"] = date.strftime("%Y-%m-%d")
        i["notes"] = "\n".join(i["notes"])
        create_time_entry(i)
        date = date + timedelta(days=1)


create_reoccurring_tasks()
