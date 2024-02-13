import jwt
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
import random
from bson.objectid import ObjectId


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
today = datetime.now()
dates = [(today - timedelta(days=i)) for i in range(30)]
habits = ['exercise', 'sleep', 'water', 'food', 'journal', 'meditation', 'reading', 'coding', 'social', 'work', 'study']
cookies = df["cookie"]
workout_values =    value = {
    "cardio": ["running", "cycling", "swimming"],
    "pull":["pull-ups", "chin-ups", "barbell rows", "barbel curl", "deadlifts"],
    "push":["push-ups", "bench press", "dumbbell press", "dips"],
    "legs": ["squats", "lunges", "calf raises", "deadlifts"]
    };

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


def upload_user_workout_types_data(user_ids, value):
    workout_types = ["pull", "push", "legs", "cardio"]
    collection = db["coll_user_workout_types"]
    all_workout_types = []
    for uid in user_ids:
        data = {key: value[f"{key}"] for key in workout_types}
        data["uid"] = uid
        all_workout_types.append(data)
    return collection.insert_many(all_workout_types).inserted_ids

# allWorkoutTypeIds = upload_user_workout_types_data(user_ids, workout_values)
# df = pd.DataFrame(allWorkoutTypeIds)
# df.to_csv("workout_type_insert_ids.csv", index=False)

def create_set(type):
    value = random.randint(1, 100)
    reps = random.randint(1, 20)
    if type == "cardio":
        return {"time": value, "reps": reps}
    return {"weight": value, "reps": reps}    

def create_exercise_data(name, type):
    no_of_sets = random.randint(3, 6)
    exercise = {"name": name, "sets": []}
    for set in range(1, no_of_sets + 1):
        exercise["sets"].append(create_set(type))
    return exercise


def upload_wokrout_data(user_ids, values):
    collection = db["coll_workout_data"]
    all_workout_data = []
    workout_types = ["pull", "push", "legs", "cardio"]
    for uid in user_ids:
        for type in workout_types:
            for date in dates:
                now = datetime.now()
                # Generate a random number of seconds between 0 and the number of seconds in 30 days
                random_seconds = random.randint(0, 30 * 24 * 60 * 60)
                # Subtract that many seconds from the current date and time
                random_date = now - timedelta(seconds=random_seconds)
                # Convert the date and time to ISO format
                # random_date_iso = random_date.isoformat()
                temp = {
                    "uid": uid,
                    "uploadDateAndTime": random_date,
                    "type": type,
                    "data": []
                }

                for exercise in values[type]:
                    temp["data"].append(create_exercise_data(exercise, type))
                all_workout_data.append(temp)
            
    return collection.insert_many(all_workout_data).inserted_ids

allWorkoutDataIDs = upload_wokrout_data(user_ids, workout_values)
df = pd.DataFrame(allWorkoutDataIDs)
df.to_csv("all_workout_data_ids.csv", index=False)



def delete_by_id(collection, ids):
    for id in ids:
        collection.delete_one({"_id": ObjectId(id)})

# insert_ids = pd.read_csv("all_workout_data_ids.csv")
# first_column = insert_ids.iloc[:, 0]
# first_column_list = first_column.tolist()

# delete_by_id(db["coll_workout_data"], first_column_list)