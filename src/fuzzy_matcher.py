import os
import pandas as pd
from fuzzywuzzy import fuzz
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the DataFrame
file_path = r"C:\Users\BSA-OliverJ'22\OneDrive\Desktop\OneDrive\Mapping\HFM Data Frame.xlsx"  # Update this path with your actual file path
df = pd.read_excel(file_path, sheet_name='Master')

def categorize_text(unstructured_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that categorizes unstructured text into fields: Current Firm, Past Firms, Name, Location."
            },
            {
                "role": "user",
                "content": f"Categorize the following information into fields: Current Firm, Past Firms, Name, Location.\n\n{unstructured_text}"
            }
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def parse_categorized_text(categorized_text):
    lines = categorized_text.split('\n')
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    return data

def fuzzy_match(parsed_data, df):
    # Mapping of parsed data keys to DataFrame columns
    column_mapping = {
        'Name': ('Name', 5),  # Higher weight for Name
        'Current Firm': ('Firm', 2),  # Medium weight for Firm
        'Past Firms': ('Prior Firm', 1),  # Lower weight for Past Firms
        'Location': ('Location', 1)  # Lower weight for Location
    }
    
    top_matches = []
    
    for i, row in df.iterrows():
        total_score = 0
        for key, value in parsed_data.items():
            if key in column_mapping:
                column, weight = column_mapping[key]
                if column in df.columns:
                    score = fuzz.ratio(value, str(row[column])) * weight
                    total_score += score
        top_matches.append((row, total_score))
    
    # Sort matches by score in descending order and keep top 3
    top_matches = sorted(top_matches, key=lambda x: x[1], reverse=True)[:3]
    
    return top_matches

def display_matches_as_table(matches):
    console = Console()
    for i, (match, score) in enumerate(matches):
        table = Table(title=f"Match #{i+1} (Total Score: {score})")
        
        # Columns to display
        columns_to_display = ['Firm', 'Name', 'Function', 'Location', 'Strategy', 'Products', 'Reports To', 'ID']
        standard_width = 30
        
        # Add specified columns with the standard width
        for column in columns_to_display:
            table.add_column(column, min_width=standard_width)
        
        # Add row with values for the specified columns
        table.add_row(*[str(match[column]) if column in match.index else '' for column in columns_to_display])
        
        console.print(table)

# Main function to get user input, categorize it, parse it, and match it against the DataFrame
def main():
    print("Enter the unstructured text to categorize. Type 'EOF' on a new line when you are done:")
    lines = []
    while True:
        line = input()
        if line.strip() == 'EOF':
            break
        lines.append(line)
    unstructured_text = " ".join(lines)

    # Categorize and parse the input text
    categorized_text = categorize_text(unstructured_text)
    print(f"Categorized text:\n{categorized_text}")
    parsed_data = parse_categorized_text(categorized_text)
    print("Parsed data:", parsed_data)

    # Perform fuzzy matching against the DataFrame
    matches = fuzzy_match(parsed_data, df)
    if matches:
        display_matches_as_table(matches)
    else:
        print("No match found.")

if __name__ == "__main__":
    main()
