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

def google_api_search(query, api_key, search_engine_id, num_results=15, advanced=False):
    result_count = 0
    start = 1
    results = []
    
    while result_count < num_results:
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&start={start}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return [f"An error occurred during the search: {response.status_code} {response.reason}"]
        
        data = response.json()
        search_items = data.get("items", [])
        
        if not search_items:
            break

        for search_item in search_items:
            if result_count >= num_results:
                break

            title = search_item.get("title", "N/A")
            snippet = search_item.get("snippet", "N/A")
            link = search_item.get("link", "N/A")

            if advanced:
                long_description = search_item.get('pagemap', {}).get('metatags', [{}])[0].get("og:description", "N/A")
                html_snippet = search_item.get("htmlSnippet", "N/A")
                
                result = (
                    f"Source {result_count+1}: Title: {title} | "
                    f"Long Description: {long_description} | "
                    f"Short Description: {snippet} | "
                    f"HTML Snippet: {html_snippet} | "
                    f"URL: {link}\n"
                )
            else:
                result = (
                    f"Source {result_count+1}: Title: {title} | "
                    f"Short Description: {snippet} | "
                    f"URL: {link}\n"
                )
            
            results.append(result)
            result_count += 1
        
        # Increment start to fetch the next batch of results
        start += 10
    
    return results
            
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

def perform_api_search(query, num_results, output_file, api, search_engine, advanced=False):
    with open(output_file, 'a') as sources:
        sources.write(f'Results for query: {query}\n\n')
        try:
            search_results = google_api_search(query, api, search_engine, num_results, advanced)
            
            # Combine all results into one line
            combined_results = "\n".join(search_results)
            sources.write(f'{combined_results}\n')
            
            if args.display:
                print(combined_results)
                
        except Exception as e:
            print(f"An error occurred during the search: {e}")
    
    return len(search_results)
        
# Perform the search and write results to a file
def perform_search(query, num_results, output_file, advanced=False, user_agent=""):
    count = 0
    with open(output_file, 'a') as sources:
        sources.write(f"Results for query: {query}\n\n")
        try:
            for source in google_search(query, num_results, advanced, user_agent=user_agent):
                sources.write(f'Source: {source}\n')
                count += 1
                if args.display:
                    print(source)
        except Exception as e:
            if e:
                print(f"An error occurred during the search: {e}")
                
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
parser.add_argument('-a', '--api-key', type=str, help="Sets Custom Search Google JSON Api key for fast non-violating queries", default="", required=False)
parser.add_argument('-seid', '--search-engine-id', type=str, help="Sets Custom Search Google JSON Api key for fast non-violating queries", default="", required=False)

args = parser.parse_args()

# Initialize variables
num_results = args.results
dork = args.query
output_file = args.output
dork_file = args.dork_file
advanced = args.info
user_agent = args.user_agent
api = args.api_key
search_engine = args.search_engine_id

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
                    if api == "" and search_engine == "":
                        try:
                            print("Running Google non api search!")
                            validate_query(dork)
                            count = perform_search(dork, num_results, output_file, extra_info=True, user_agent=user_agent)
                            print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                            time.sleep(random.randint(10, 50))
                        except ValueError as e:
                            print(f"Error: {e}")
                            
                    elif api != "" and search_engine != "":
                        try:
                            print("Running Google custom api search!")
                            validate_query(dork)
                            count = perform_api_search(dork, num_results, output_file, api, search_engine, advanced=True)
                            time.sleep(random.randint(10, 50))
                        except ValueError as e:
                            print(f"Error: {e}")

                    else:
                        print("Error! API Key and Search Engine ID must both be included if one is listed!")
                        exit(1)     
                    
                else:
                    if api == "" and search_engine == "":
                        try:
                            print("Running Google non api search!")
                            time.sleep(random.randint(10, 50))
                            validate_query(dork)
                            count = perform_search(dork, num_results, output_file, advanced=advanced, user_agent=user_agent)
                            print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                            time.sleep(random.randint(10, 50))
                        except ValueError as e:
                            print(f"Error: {e}")
                            
                    elif api != "" and search_engine != "":
                        try:
                            print("Running Google custom api search!")
                            validate_query(dork)
                            count = perform_api_search(dork, num_results, output_file, api, search_engine, advanced=True)
                            time.sleep(random.randint(10, 50))
                        except ValueError as e:
                            print(f"Error: {e}")

                    else:
                        print("Error! API Key and Search Engine ID must both be included if one is listed!")
                        exit(1)  
else:
    if not dork:
        print("Error: No query provided. Use -q to specify a search query.")
        exit(1)
    
    if api == "" and search_engine == "":
        validate_query(dork)
        count = perform_search(dork, num_results, output_file, advanced=advanced, user_agent=user_agent)
    
    elif api != "" and search_engine != "":
        print("Running Google custom api search!")
        validate_query(dork)
        count = perform_api_search(dork, num_results, output_file, api, search_engine, advanced)
        
    else:
        print("Error! API Key and Search Engine ID must both be included if one is listed!")
        exit(1)
    
    print(f"\nNumber of results found for query '{dork}': {count}")

print(f"Results saved to {output_file}")


# # Download the files listed in 'sources.txt'
# with open('sources.txt', 'r') as sources:
#     for source in sources:
#         source = source.strip()
#         if source:
#             os.system(f"curl -o ~/Desktop/sources/ {source}")
