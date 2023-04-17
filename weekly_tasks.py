from dotenv import dotenv_values

config = dotenv_values(".env")

PROJECT_ID = config.get("PROJECT_ID")
PROJECT_TASK_ID = config.get("PROJECT_TASK_ID")
GM_PROJECT_ID = config.get("GM_PROJECT_ID")
GM_MISC_NON_BILLABLE_TASK_ID = config.get("GM_MISC_NON_BILLABLE_TASK_ID")
GM_PTO_HOLIDAY_TASK_ID = config.get("GM_PTO_HOLIDAY_TASK_ID")

WEEKLY_TASKS = [
    # MONDAY
    [
        {
            "project_id": PROJECT_ID,
            "task_id": PROJECT_TASK_ID,
            "hours": "8",
            "notes": ["GM Standup", "Internal Huddle", "Stripe Weekly Call","Artemis Prod/Eng Collaboration", "Code Freeze Targets", "Sprint Planning"],
        }
    ],
    # TUESDAY
    [
        {
            "project_id": PROJECT_ID,
            "task_id": PROJECT_TASK_ID,
            "hours": "8",
            "notes": ["TP-13732 Sync", "Friendly order ID sync", "Artemis Integration Sync", "Dev Standup", "Sprint Planning"],
        }
    ],
    # WEDNESDAY
    [
        {
            "project_id": PROJECT_ID,
            "task_id": PROJECT_TASK_ID,
            "hours": "7",
            "notes": ["Artemis Huddle", "MAM Sync", "Sprint Review and Demo", "Leadership Check-In", "Sprint Retro", "Redox Weekly Connect"],
        },
        {
            "project_id": GM_PROJECT_ID,
            "task_id": GM_MISC_NON_BILLABLE_TASK_ID,
            "hours": "1",
            "notes": ["Intro to DevOps"],
        },
    ],
    # THURSDAY
    [
        {
            "project_id": PROJECT_ID,
            "task_id": PROJECT_TASK_ID,
            "hours": "8",
            "notes": ["Artemis Regroup","Tech Leads Sync", "Dev Standup", "Artemis Integration Sync"],
        }
    ],
    # FRIDAY
    [
        {
            "project_id": PROJECT_ID,
            "task_id": PROJECT_TASK_ID,
            "hours": "7",
            "notes": ["GM Standup", "Internal Huddle", "Project Touchbase", "Mailing Server Infra Sync"],
        },
        {
            "project_id": GM_PROJECT_ID,
            "task_id": GM_MISC_NON_BILLABLE_TASK_ID,
            "hours": "1",
            "notes": ["Mentorship Working Group Standup"],
        },
    ],
]
