#!/usr/bin/env python3
import os
import random
import subprocess
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def read_number():
    with open('number.txt', 'r') as f:
        return int(f.read().strip())

def write_number(num):
    with open('number.txt', 'w') as f:
        f.write(str(num))

def git_commit():
    subprocess.run(['git', 'add', 'number.txt'], check=True)
    date = datetime.now().strftime('%Y-%m-%d')
    commit_message = f"Update number: {date}"
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)

def git_push():
    try:
        subprocess.run(['git', 'push'], check=True, capture_output=True, text=True)
        print("Changes pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print("Error pushing to GitHub:")
        print(e.stderr)

def update_cron_with_random_time():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    task_name = "DailyNumberIncrementer"
    task_command = f"schtasks /create /tn {task_name} /tr \"python {os.path.join(script_dir, 'update_number.py')}\" /sc daily /st {random_hour:02d}:{random_minute:02d} /f"
    result = subprocess.run(task_command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Cron job updated to run at {random_hour:02d}:{random_minute:02d} daily.")
    else:
        print(f"Failed to update Task Scheduler: {result.stderr}")

def main():
    try:
        current_number = read_number()
        new_number = current_number + 1
        write_number(new_number)
        git_commit()
        git_push()
        update_cron_with_random_time()
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
