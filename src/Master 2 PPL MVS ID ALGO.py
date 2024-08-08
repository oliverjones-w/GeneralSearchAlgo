import os
import pandas as pd
from fuzzywuzzy import fuzz
import xlsxwriter
from openpyxl import Workbook

# Load the data frames
id_list_file_path = "C:\\Users\\Bay Street - Larry B\\Documents\\Brielle\\Programming\\Projects\\GeneralSearchAlgo\\Workbooks\\IRMUniqueIDs.txt"

irm_path = "K:\Market Maps\Interest Rates Map (K-Drive) (EXPERIMENTAL).xlsm"
xls = pd.ExcelFile(irm_path)
df_irm_master = pd.read_excel(xls, sheet_name='Master', header=2)
df_irm_people_moves = pd.read_excel(xls, sheet_name='People Moves', header=2)

# Converted macro code
def generate_unique_id(existingIDs):
    maxNumber = 0000000
    
    for id in existingIDs:
        if len(id) != 0:
            numericComp = int(id[3:])
            if numericComp > maxNumber:
                maxNumber = numericComp
    
    return f"IR_{maxNumber + 1:07d}"


def read_ids_from_file(id_list_file_path):
    file_series = pd.read_csv(id_list_file_path, header=None)
    list = file_series[0].tolist()
    
    return list
    
def write_id_to_file(id_list_file_path, id):
    with open(id_list_file_path, 'a') as file:
        file.write('\n' + id)


def fill_blank_ids():
    id_col = df_irm_master['ID']
    
    # Read existing IDs from the file
    existing_ids = read_ids_from_file(id_list_file_path)
    # Iterate over the column and fill in blank cells
    for index, cell in id_col.items():
        if pd.isna(cell):
            new_id = generate_unique_id(existing_ids)
            df_irm_master.at[index, 'ID'] = new_id
            
            # Append the new ID to the list of existing IDs
            existing_ids.append(new_id)
            
            # Write  new ID to the txt file
            write_id_to_file(id_list_file_path, new_id)
        


# Function to split and get last name

def get_last_name(full_name):
    return full_name.split()[-1].lower()

# Function to perform fuzzy matching
def fuzzy_match(row, df_master):
    column_mapping = {    
        'Current Firm': ('Firm', 3),
        'Former Firm': ('Prior Firm', 2),
        'Current Title': ('Title AMALG', 3), 
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
"""
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
"""

# Save the matched DataFrame to a new Excel workbook
with pd.ExcelWriter("k:\Market Maps\Interest Rates Map (K-Drive) (EXPERIMENTAL) - Copy.xlsm", engine='openpyxl') as writer:
    df_irm_master.to_excel(writer, sheet_name='Master', index=False)
    # matched_df.to_excel(writer, sheet_name='Matched Data', index=False)