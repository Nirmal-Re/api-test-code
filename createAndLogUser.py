# import csv
# import faker

# # Create a Faker instance
# fake = faker.Faker()

# # Define the header
# header = ['email', 'password', 'firstName', 'lastName']

# # Generate the data
# data = []
# for _ in range(20):  # Generate 100 rows of data
#     email = fake.email()
#     password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     data.append([email, password, first_name, last_name])

# # Write the data to a CSV file
# with open('users.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     # writer.writerow(header)
#     writer.writerows(data)


import csv
import requests
import faker
import json

# Create a Faker instance
fake = faker.Faker()

# Define the header
header = ['email', 'password', 'lastName', 'firstName', 'cookie']

# URL for registration and login
host = 'http://172.167.242.26'
register_url = f'{host}/auth/register'
login_url = f'{host}/auth/login'
headers = {'Content-Type': 'application/json'}


# Prepare the CSV file
with open('users.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    # Generate and register users
    for _ in range(20):  # Generate 100 users
        email = fake.email()
        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        first_name = fake.first_name()
        last_name = fake.last_name()



        register_data = {'email': email, 'password': password, 'firstName': first_name, 'lastName': last_name}
        register_response = requests.post(register_url, data=json.dumps(register_data), headers=headers)

        # If registration was successful, log in the user
        if register_response.status_code == 200:
            login_data = {'email': email, 'password': password}
            login_response = requests.post(login_url, data=json.dumps(login_data), headers=headers)

            # If login was successful, save the user's cookie
            if login_response.status_code == 200:
                print(login_response)
                cookie = login_response.cookies['access_token']  # Replace 'cookie_name' with the actual cookie name
                writer.writerow([email, password, last_name, first_name, cookie])