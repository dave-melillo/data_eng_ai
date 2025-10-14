import re  #A

# Example log entries  #B
logs = [  #C
    "ERROR 2025-06-09 12:34:56 Server failed to respond",  #D
    "INFO 2025-06-09 12:35:56 User logged in",  #E
    "WARNING 2025-06-09 12:36:56 Disk space low"  #F
]

# Multi-part pattern with capture groups  #G
pattern = r"(ERROR|INFO|WARNING)\s(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})"  #H

# Extract log type, date, and time from each log entry  #I
for log in logs:  #J
    match = re.search(pattern, log)  #K
    if match:  #L
        log_type, date, time = match.groups()  #M
        print(f"Type: {log_type}, Date: {date}, Time: {time}")  #N

#A Import required libraries for regex operations.
#B–#F Define example log entries to simulate real-world scenarios.
#G–#H Create a regex pattern to capture log type, date, and time components.
#I–#N Iterate over log entries to extract and print each component using regex. 