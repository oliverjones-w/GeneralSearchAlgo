import os
import pandas as pd
from fuzzywuzzy import fuzz
import xlsxwriter
from openpyxl import Workbook


# Load the data frames
irm_file_path = "K:\Market Maps\Interest Rates Map (K-Drive).xlsm"

df_master = pd.read_excel(irm_file_path, sheet_name='Master', header=2, engine='openpyxl')
df_people_moves = pd.read_excel(irm_file_path, sheet_name='People Moves', header=2, engine='openpyxl')

print(df_master.columns)
print(df_people_moves.columns)

# Function to split and get last name

def get_last_name(full_name):
    return full_name.split()[-1].lower()

# Function to perform fuzzy matching
def fuzzy_match(row, df_master):
    column_mapping = {    
        'Current Firm': ('Firm', 3),
        'Former Firm': ('Prior Firm', 2),
        'Current Title': ('Title', 3), 
        'Current Location': ('Location', 1)
    }   

    highest_score = 0
    best_match = None
    row_last_name = get_last_name(row['Name'])

    for _, master_row in df_master.iterrows():
        master_last_name = get_last_name(master_row['Name'])
        
        # Ensure last names match
        if row_last_name != master_last_name:
            continue

        # Compute first name similarity
        first_name_score = fuzz.ratio(row['Name'].split()[0], master_row['Name'].split()[0]) * 9

        total_score = first_name_score
        for key, (column, weight) in column_mapping.items():
            score = fuzz.ratio(str(row[key]), str(master_row[column])) * weight
            total_score += score

        if total_score > highest_score:
            highest_score = total_score
            best_match = master_row

    return best_match, highest_score

# Set the threshold for the best match
threshold = 800

# List to store the matched rows
matched_rows = []

# Perform fuzzy matching for each row in People Moves
for index, row in df_people_moves.iterrows():
    if index >= 4376:
        break
    print(f"Processing row {index + 1}/{len(df_people_moves)}: {row['Name']}")
    best_match, score = fuzzy_match(row, df_master)
    if score > threshold:
        row['Matched ID'] = best_match['ID']
        print(f"Match found for row {index + 1}: {best_match['ID']} with score {score}")
        matched_rows.append(row)
    else:
        print(f"No suitable match found for row {index + 1}")

# Create a DataFrame from the matched rows
matched_df = pd.DataFrame(matched_rows)


# Save the matched DataFrame to a new Excel workbook
with pd.ExcelWriter("K:\Market Maps\Output2.xlsx", engine='openpyxl') as writer:
    matched_df.to_excel(writer, sheet_name='Sheet1', index=False)

# "k:\Market Maps\Interest Rates Map (K-Drive) (EXPERIMENTAL).xlsm"