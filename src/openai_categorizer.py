import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Main function to get user input and categorize it
def main():
    print("Enter the unstructured text to categorize. Type 'EOF' on a new line when you are done:")
    lines = []
    while True:
        line = input()
        if line.strip() == 'EOF':
            break
        lines.append(line)
    unstructured_text = " ".join(lines)
    categorized_text = categorize_text(unstructured_text)
    print(f"Categorized text:\n{categorized_text}")
    parsed_data = parse_categorized_text(categorized_text)
    print("Parsed data:", parsed_data)

if __name__ == "__main__":
    main()

