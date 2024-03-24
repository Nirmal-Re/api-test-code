import pandas as pd

# Load the CSV data into a DataFrame
data = pd.read_csv('secondResponse.csv')

# Calculate throughput
total_requests = len(data["elapsed"])
total_time_seconds = (data['timeStamp'].max() - data['timeStamp'].min()) / 1000  # Convert milliseconds to seconds
throughput = total_requests / 60

# Calculate average latency
average_latency = data['Latency'].mean()

print(throughput, total_requests, total_time_seconds)
print("Throughput: {:.2f} requests per second".format(throughput))
print("Average Latency: {:.2f} milliseconds".format(average_latency))