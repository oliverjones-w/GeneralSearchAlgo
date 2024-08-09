"""

import os
import pandas as pd
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
        

# Save the matched DataFrame to a new Excel workbook
with pd.ExcelWriter("k:\Market Maps\Interest Rates Map (K-Drive) (EXPERIMENTAL) - Copy.xlsm", engine='openpyxl') as writer:
    df_irm_master.to_excel(writer, sheet_name='Master', index=False)

"""