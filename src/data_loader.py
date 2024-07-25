import pandas as pd

def load_excel_to_dataframe(file_path):
    df = pd.read_excel(file_path, sheet_name='Master')
    return df

if __name__ == "__main__":
    file_path = r"C:\Users\BSA-OliverJ'22\OneDrive\Desktop\OneDrive\Mapping\Hedge Fund Map (Personal).xlsm"
    df = load_excel_to_dataframe(file_path)
    print(df.head())

    