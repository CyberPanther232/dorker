"""
Program: dorker.py
Date Created: 28-Aug-2024
Date Modified: 30-Aug-2024
Purpose: To automate Google search queries or Google dorks when looking for OSINT (open-source intelligence) or just looking for general source
"""

# Necessary libraries
import random
import requests
import os
import argparse
import time
import requests
from bs4 import BeautifulSoup

def google_search(query, num_results=15, advanced=False, user_agent=""):
    if user_agent != "":
        headers = {
            'User-Agent': f'{user_agent}'
        }
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }

    search_url = f"https://www.google.com/search?q={query}&num={num_results}"

    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve search results: Status Code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    print("Response Text:", response.text[:1000])

    search_results = []
    for result in soup.find_all('div', class_='g'):
        title_element = result.find('h3')
        description_element = result.find('span', class_='aCOpRe')
        link_element = result.find('a', href=True)

        if title_element and description_element and link_element and advanced:
            title = title_element.text
            description = description_element.text
            link = link_element['href']

            search_results.append({
                'Title': title,
                'Description': description,
                'Link': link
            })
        elif link_element:
            search_results.append(link_element['href'])

    # Debugging: Print the parsed results
    print("Parsed Results:", search_results)

    return search_results


def validate_query(query):
    """Ensure the search query is valid and non-empty."""
    if not query or len(query.strip()) == 0:
        raise ValueError("Search query cannot be empty.")
    else:
        return + 1

def check_network():
    """Check if the network connection is working."""
    try:
        response = requests.get('https://www.google.com', timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Network check failed: {e}")
        return False

# Perform the search and write results to a file
def perform_search(query, num_results, output_file, extra_info=False, user_agent=""):
    count = 0
    with open(output_file, 'a') as sources:
        sources.write(f"\nResults for query: {query}\n\n")
        try:
            for source in google_search(query, num_results, advanced=extra_info, user_agent=user_agent):
                if extra_info:
                    sources.write(f'Source: {source}\n')
                    count += 1
                    if args.display:
                        print(source)
                else:
                    sources.write(f'Source: {source}\n')
                    count += 1
                    if args.display:
                        print(source)
        except Exception as e:
            if e:
                print(f"An error occurred during the search: {e}")
                print("\nAdding buffer time between search queries...")
                buffer = random.randint(0, 15) ** 2
                print(f"Waiting {buffer} seconds before trying another...")
                time.sleep(buffer)
            else:
                print(f"An error occurred during the search: {e}")
                pass
    return count


parser = argparse.ArgumentParser(
    prog="dorker.py",
    description="Takes in Google search queries (particularly dork queries) and then places the results in a file"
)

parser.add_argument('-r', '--results', default=15, type=int, help="Sets the maximum number of results", required=False)
parser.add_argument('-q', '--query', type=str, help="Google search query or dork query to find results for", required=False)
parser.add_argument('-o', '--output', default='sources.txt', type=str, help="Sets the name of the output file", required=False)
parser.add_argument('-d', '--display', action='store_true', help="Displays/prints the URLs from the query results", required=False)
parser.add_argument('-i', '--info', action='store_true', help="Gathers advanced information such as title and description", required=False)
parser.add_argument('-df', '--dork-file', type=str, help="Reads file with queries to run multiple queries at once", default="", required=False)
parser.add_argument('-u', '--user-agent', type=str, help="Allows setting custom User-Agent string header (not recommended)", default="", required=False)

args = parser.parse_args()

# Initialize variables
num_results = args.results
dork = args.query
output_file = args.output
dork_file = args.dork_file
advanced = args.info
user_agent = args.user_agent

# Validate the input
try:
    if dork:
        validate_query(dork)
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

# Check network connectivity
if not check_network():
    print("Error: No network connection. Please check your internet connection.")
    exit(1)

# If a dork file is specified, process each query from the file
if dork_file:
    if not os.path.isfile(dork_file):
        print(f"Error: The file {dork_file} does not exist.")
        exit(1)
    with open(dork_file, 'r') as file:
        for line in file:
            dork = line.strip()
            if dork:
                if args.info:
                    try:
                        time.sleep(random.randint(10, 50))
                        validate_query(dork)
                        count = perform_search(dork, num_results, output_file, True, user_agent=user_agent)
                        print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    try:
                        time.sleep(random.randint(10, 50))
                        validate_query(dork)
                        count = perform_search(dork, output_file)
                        print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                    except ValueError as e:
                        print(f"Error: {e}")
else:
    if not dork:
        print("Error: No query provided. Use -q to specify a search query.")
        exit(1)
    count = perform_search(dork, num_results, output_file, extra_info=advanced, user_agent=user_agent)
    print(f"\nNumber of results found for query '{dork}': {count}")

print(f"Results saved to {output_file}")


# # Download the files listed in 'sources.txt'
# with open('sources.txt', 'r') as sources:
#     for source in sources:
#         source = source.strip()
#         if source:
#             os.system(f"curl -o ~/Desktop/sources/ {source}")
