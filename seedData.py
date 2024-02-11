import jwt
import pandas as pd
import datetime
from pymongo import MongoClient
import random



# Get today's date
#TODO: ALLOW TH USER TO SPECIFY IF THE APP IS MONOLITHIC OR NOT FROM THE COMMAND LINE RATHER THAN STACTICALLY DEFINING IT HERE.
# import argparse


# parser = argparse.ArgumentParser(description='Seed data for the app')

# parser.add_argument('--micro', default=false, action='store_true', help='To specify if the app is monolithic or not.')

# args = parser.parse_args()


#DATA TO REMEMBER so each run of this file pushes same data to the database
habits_data = []
logs_data = []
workout_types_data = []
workout_data = []

#connect to the mongo database
client = MongoClient('mongodb://localhost:27017/')
db = client['habit_tracker']

# Load the jwt tokens from the users. And retrieve the user ID.
micro = False
df = pd.read_csv('users.csv')
user_ids = []
today = datetime.datetime.now()
dates = [(today - datetime.timedelta(days=i)).isoformat() for i in range(30)]
habits = ['exercise', 'sleep', 'water', 'food', 'journal', 'meditation', 'reading', 'coding', 'social', 'work', 'study']
cookies = df["cookie"]

#SETTING USER IDS
for i, cookie in enumerate(cookies):
        user_id = jwt.decode(cookie, algorithms=['HS256'], options={"verify_signature": False})['uid']
        user_ids.append(user_id)

#SETTING HABITS FOR ALL USERS

def upload_user_habit_data(user_ids):
    collection= db["coll_user_habits"]
    for uid in user_ids:
        data = {
        "uid": uid,
        "habits": habits    
        }
        habits_data.append(data)
        collection.insert_one(data)


def delete_user_habit_data():
    for uid in user_ids:
        collection = db["coll_user_habits"]
        collection.delete_many({"uid": uid})

def upload_user_logs_data(user_ids, habits, dates):
    collection = db["coll_logs"]
    all_logs = [] #TODO check if data already exists in seed data
    for uid in user_ids:
        for date in dates:
            log = {key: random.choice([True, False]) for key in habits}
            log["uid"] = uid
            log["moods"] = [random.choice([True, False]) for _ in range(len(habits))]
            log["uploadDateAndTime"] = date
            all_logs.append(log)
    return collection.insert_many(all_logs).inserted_ids
            

# allInsertIds = upload_user_logs_data(user_ids, habits, dates)
# df = pd.DataFrame(allInsertIds)
# df.to_csv("log_insert_ids.csv", index=False)


def upload_user_workout_types_data(user_ids):
    workout_types = ["pull", "push", "legs", "cardio"]
    value = {
    "cardio": ["running", "cycling", "swimming"],
    "pull":["pull-ups", "chin-ups", "barbell rows", "barbel curl", "deadlifts"],
    "push":["push-ups", "bench press", "dumbbell press", "dips"],
    "legs": ["squats", "lunges", "calf raises", "deadlifts"]
    }
    collection = db["coll_workout_types"]
    all_workout_types = []
    for uid in user_ids:
        data = {key: value[f"{key}"] for key in workout_types}
        data["uid"] = uid
        all_workout_types.append(data)
    return collection.insert_many(all_workout_types).inserted_ids

# allWorkoutTypeIds = upload_user_workout_types_data(user_ids)
# df = pd.DataFrame(allWorkoutTypeIds)
# df.to_csv("workout_type_insert_ids.csv", index=False)

