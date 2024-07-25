import openai
import os
import sys
import pandas as pd
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import threading
import time

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from file_monitor import monitor_file, load_excel_to_dataframe

#load the environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#load the excel file into the dataframe
file_path = r"C:\Users\BSA-OliverJ'22\OneDrive\Desktop\OneDrive\Mapping\Hedge Fund Map (Personal).xlsm"
df = load_excel_to_dataframe(file_path)

#print the headers
print("Initial DataFrame:")
print(df.head())

# Update the dataframe when the file is modified
def on_file_update():
    global df
    try:
        df = load_excel_to_dataframe(file_path)
        print("Updated DataFrame:")
        print(df.head())
    except Exception as e:
        print(f"An error occurred while updating the dataframe: {e}")

# Monitor the Excel file for changes
file_monitor_thread = threading.Thread(target=monitor_file, args=(file_path, on_file_update))
file_monitor_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

print("Script terminated.")