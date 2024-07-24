import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify the API key
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {'Set' if api_key else 'Not Set'}")

# Initialize the OpenAI client
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
else:
    client = OpenAI(api_key=api_key)
    print("API Key is set")

# Function to interact with OpenAI API and print raw response
def categorize_data(unstructured_text):
    examples = """
    Please categorize the following information into "Position" and "Education" sections.
    For each "Position," include the Firm, Title, Start Year, and End Year in the format:
    | Firm (String) | Title (String) | Start Year (YYYY) | End Year (YYYY or 'Present') |.
    For each "Education," include the Degree, School, and Graduation Year in the format:
    | Degree (String) | School (String) | Graduation Year (YYYY) |.
    If any information is not available, leave the corresponding cell blank. Do not infer or guess any information.

    Example:

    Input:
    Manish Agarwal Goldman Sachs
    (New York, NY)
    Vice President
    ▪ TBA Trading; Goldman Sachs (2021 – Present)
    ▪ Market Risk, US Mortgages & Credit; Goldman Sachs (2018 – 2021)
    ▪ Founding Member; MKS Capital (2012 – 2018)
    ▪ Nomura (2009 – 2012)
    ▪ Lehman Brothers (2001 – 2008)
    ▪ MBA, Indian Institute of Management Bangalore (2001)

    Output:

    ### Position

    | Firm            | Title                                     | Start Year | End Year   |
    |-----------------|-------------------------------------------|------------|------------|
    | Goldman Sachs   | Vice President, TBA Trading               | 2021       | Present    |
    | Goldman Sachs   | Market Risk, US Mortgages & Credit        | 2018       | 2021       |
    | MKS Capital     | Founding Member                           | 2012       | 2018       |
    | Nomura          |                                            | 2009       | 2012       |
    | Lehman Brothers |                                            | 2001       | 2008       |

    ### Education

    | Degree | School                               | Graduation Year |
    |--------|--------------------------------------|-----------------|
    | MBA    | Indian Institute of Management Bangalore | 2001         |

    Input:
    {unstructured_text}

    Output:
    
    """

    prompt = examples + "\n" + unstructured_text

    response = client.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    extracted_text = response.choices[0].text.strip()
    print("Raw response from API:")
    print(extracted_text)
    return extracted_text

# Function to parse the extracted text
def parse_extracted_text(extracted_text):
    data = {
        "Position": [],
        "Education": []
    }
    lines = extracted_text.split("\n")
    section = None
    
    for line in lines:
        if "### Position" in line:
            section = "Position"
            continue
        elif "### Education" in line:
            section = "Education"
            continue
        
        if section == "Position" and "|" in line:
            parts = line.split("|")
            if len(parts) == 5:
                firm, title, start_year, end_year = parts[1], parts[2], parts[3], parts[4]
                data["Position"].append({
                    "Firm": firm.strip(),
                    "Title": title.strip(),
                    "Start Year": start_year.strip(),
                    "End Year": end_year.strip()
                })
        
        if section == "Education" and "|" in line:
            parts = line.split("|")
            if len(parts) == 4:
                degree, school, graduation_year = parts[1], parts[2], parts[3]
                data["Education"].append({
                    "Degree": degree.strip(),
                    "School": school.strip(),
                    "Graduation Year": graduation_year.strip()
                })
    
    return data

# Function to test the categorize_data function in the terminal
def test_categorize_data():
    while True:
        prompt = input("Enter the text to categorize (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        extracted_text = categorize_data(prompt)
        parsed_data = parse_extracted_text(extracted_text)
        print("Extracted Data:")
        for section, entries in parsed_data.items():
            print(f"### {section}")
            for entry in entries:
                print(entry)

if __name__ == "__main__":
    test_categorize_data()
