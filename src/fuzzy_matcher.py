import os
import pandas as pd
from fuzzywuzzy import process
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the DataFrame
file_path = r"C:\Users\BSA-OliverJ'22\OneDrive\Desktop\OneDrive\Mapping\HFM Data Frame.xlsx"  # Update this path with your actual file path
df = pd.read_excel(file_path, sheet_name='Master')

# Print the DataFrame to verify it is loaded correctly
print("DataFrame loaded:")
print(df.head())

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
        'Name': 'Name',
        'Current Firm': 'Firm',
        'Past Firms': 'Prior Firm',
        'Location': 'Location'
    }
    matches = {}
    for key, value in parsed_data.items():
        column = column_mapping.get(key)
        if column and column in df.columns:
            best_match = process.extractOne(value, df[column], score_cutoff=80)  # Using a score cutoff to ensure relevance
            matches[key] = best_match
    return matches

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
    print("Fuzzy matches:", matches)

if __name__ == "__main__":
    main()
