from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB("standup_logs.json")

def save_update(sprint, date, member_name, yesterday, today, blocker):
    db.insert({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sprint": sprint,
        "date": date,
        "member_name": member_name,
        "yesterday": yesterday,
        "today": today,
        "blocker": blocker
    })

def get_updates_by_day(sprint, date):
    q = Query()
    return db.search((q.sprint == sprint) & (q.date == date))

def get_updates_by_sprint(sprint):
    q = Query()
    return db.search(q.sprint == sprint)