import requests
from bs4 import BeautifulSoup
import time
import json
import re

# Retry mechanism and data scraping function
def fetch_data_with_retries(url, retries=3, delay=2):
    """
    Try → Fail → Wait → Try again → Repeat until success or retries finish
    """
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))  # Exponential backoff
            else:
                raise


# Function to extract data using BeautifulSoup and regex
def extract_data_from_html(html_content):
    """
    Extract links containing the word 'python'
    """
    if not html_content:
        raise ValueError("HTML content is empty or invalid")

    soup = BeautifulSoup(html_content, "html.parser")
    titles = []

    for link in soup.find_all("a", href=True):
        title = link.get_text(strip=True)

        if re.search(r"python", title, re.IGNORECASE):
            titles.append(title)

    return titles


# Function to save data to JSON file
def save_data_to_json(data, filename="scraped_data.json"):
    """
    Save extracted data into a JSON file
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4) #white space ie the space that uh give in  start of output inscrapped data json file !

        print(f"Data has been saved to {filename}")

    except Exception as e:
        print(f"Error saving data: {e}")


# URL to scrape
url = "https://docs.python.org/3/"

# Fetch, extract, and save
html_content = fetch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data)
