import jwt
import json
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
all_data = {
    "habits_data": [],
    "logs_data": [],
    "workout_types_data": [],
    "workout_data": []
}

try:
    with open('all_data.json', 'r') as f:
        file_data = json.load(f)
        all_data.update(file_data)

except (FileNotFoundError, json.JSONDecodeError):
    print("No file found or file is empty.")
    pass



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

def upload_user_habit_data(user_ids, habits):
    collection= db["coll_user_habits"]
    all_habits_docs = []
    if len(all_data["habits_data"]) > 0:
        print("Data already exists")
        for habits in all_data["habits_data"]:
            del habits["_id"]
        insert_ids = collection.insert_many(all_data["habits_data"]).inserted_ids
        df = pd.DataFrame(insert_ids)
        df.to_csv("coll_user_habits.csv", index=False)
        return True
    else:
        for uid in user_ids:
            data = {
            "uid": uid,
            "habits": habits    
            }
            all_data["habits_data"].append(data)
            all_habits_docs.append(data)
        insert_ids = collection.insert_many(all_habits_docs).inserted_ids
        df = pd.DataFrame(insert_ids)
        df.to_csv("coll_user_habits.csv", index=False)
        return True

    
def upload_user_logs_data(user_ids, habits, dates):
    collection = db["coll_logs"]
    all_logs = []
    if len(all_data["logs_data"]) > 0:
        print("Data already exists")
        all_data["logs_data"] = all_data["logs_data"]
        for logs in all_data["logs_data"]:
            logs["uploadDateAndTime"] = datetime.strptime(logs["uploadDateAndTime"],'%Y-%m-%dT%H:%M:%S.%f')
            del logs["_id"]
        insert_ids = collection.insert_many(all_data["logs_data"]).inserted_ids
        df = pd.DataFrame(insert_ids)
        df.to_csv("coll_logs.csv", index=False)
        return True
    
    #Create Dummy Data and upload to the database
    for uid in user_ids:
        for date in dates:
            log = {key: random.choice([True, False]) for key in habits}
            log["uid"] = uid
            log["moods"] = [random.choice([True, False]) for _ in range(len(habits))]
            log["uploadDateAndTime"] = date
            all_logs.append(log)
    all_data["logs_data"] = all_logs
    insert_ids = collection.insert_many(all_logs).inserted_ids
    df = pd.DataFrame(insert_ids)
    df.to_csv("coll_logs.csv", index=False)
    return True
            

def upload_user_workout_types_data(user_ids, value):
    workout_types = ["pull", "push", "legs", "cardio"]
    collection = db["coll_user_workout_types"]
    all_workout_types = []
    if len(all_data["workout_types_data"]) > 0:
        print("Data already exists")
        all_data["workout_types_data"] = all_data["workout_types_data"]
        for workout in all_data["workout_types_data"]:
            del workout["_id"]
        insert_ids = collection.insert_many(all_data["workout_types_data"]).inserted_ids
        df = pd.DataFrame(insert_ids)
        df.to_csv("coll_user_workout_types.csv", index=False)
        return True
    #create Dummy Data
    for uid in user_ids:
        data = {key: value[f"{key}"] for key in workout_types}
        data["uid"] = uid
        all_workout_types.append(data)
    all_data["workout_types_data"] = all_workout_types
    insert_ids = collection.insert_many(all_workout_types).inserted_ids
    df = pd.DataFrame(insert_ids)
    df.to_csv("coll_user_workout_types.csv", index=False)
    return True



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


def upload_workout_data(user_ids, values):
    collection = db["coll_workout_data"]
    all_workout_data = []
    workout_types = ["pull", "push", "legs", "cardio"]
    if len(all_data["workout_data"]) > 0:
        print("Data already exists")
        all_data["workout_data"] = all_data["workout_data"]
        for workout in all_data["workout_data"]:
            workout["uploadDateAndTime"] = datetime.strptime(workout["uploadDateAndTime"],'%Y-%m-%dT%H:%M:%S.%f')
            del workout["_id"]
        insert_ids = collection.insert_many(all_data["workout_data"]).inserted_ids
        df = pd.DataFrame(insert_ids)
        df.to_csv("coll_workout_data.csv", index=False)
        return True
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
    all_data["workout_data"] = all_workout_data   
    insert_ids = collection.insert_many(all_workout_data).inserted_ids
    df = pd.DataFrame(insert_ids)
    df.to_csv("coll_workout_data.csv", index=False)
    return True



def delete_by_id(collection, ids):
    for id in ids:
        collection.delete_one({"_id": ObjectId(id)})



def delete_previous_upload_data(coll_names):
    for coll_name in coll_names:
        insert_ids = pd.read_csv(f"{coll_name}.csv")
        first_column = insert_ids.iloc[:, 0].tolist()
        delete_by_id(db[coll_names], first_column)
    
        
def delete_all(collection_name):
    collection = db[collection_name]
    collection.delete_many({})


upload_user_habit_data(user_ids, habits)
upload_user_logs_data(user_ids, habits, dates)
upload_user_workout_types_data(user_ids, workout_values)
upload_workout_data(user_ids, workout_values)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

# Open the JSON file
with open('all_data.json', 'w') as f:
    # Write the data to the file
   f.write(JSONEncoder().encode(all_data))

# delete_all("coll_user_habits")
# delete_all("coll_logs")
# delete_all("coll_user_workout_types")
# delete_all("coll_workout_data")