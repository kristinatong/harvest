from dotenv import load_dotenv, dotenv_values
from requests import PreparedRequest, get, post
from datetime import datetime, timedelta
from weekly_tasks import WEEKLY_TASKS
import pprint

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
        return results.get("time_entries", [])


def is_time_entry_last_30_days(time_entry):
    now = datetime.now()
    spent_date = datetime.strptime(time_entry.get("spent_date"), "%Y-%m-%d")
    last_month_date = now - timedelta(days=15)

    if spent_date > last_month_date:
        return True
    else:
        return False


def get_relevant_project_ids_this_year():
    all_time_entries = get_time_entries()
    recent_time_entries = list(filter(is_time_entry_last_30_days, all_time_entries))
    codes = {}

    for time_entry in recent_time_entries:
        client = time_entry.get("client")
        project = time_entry.get("project")
        task = time_entry.get("task")

        client_name = client.get("name")
        client_id = client.get("id")
        project_name = project.get("name")
        project_id = project.get("id")
        task_id = task.get("id")
        task_name = task.get("name")

        if codes.get(client_name) is None:
            codes[client_name] = {
                "client_id": client_id,
                project_name: {"project_id": project_id, "tasks": {task_name: task_id}}
            }
        elif codes.get(client_name).get(project_name) is None:
            codes[client_name][project_name] = {
                "project_id": project_id,
                "tasks": {task_name: task_id},
            }
        else:
            codes[client_name][project_name]["tasks"][task_name] = task_id

    pprint.pprint(codes)


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
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    date = monday

    for tasks in WEEKLY_TASKS:
        spent_date = date.strftime("%Y-%m-%d")
        for t in tasks:
            t["spent_date"] = spent_date
            t["notes"] = "\n".join(t["notes"])
            create_time_entry(t)
        date = date + timedelta(days=1)


get_relevant_project_ids_this_year()
# create_recurring_tasks()
