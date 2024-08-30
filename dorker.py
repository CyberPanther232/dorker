"""
Program: dorker.py
Date Created: 28-Aug-2024
Date Modified: 29-Aug-2024
Purpose: To automate Google search queries or Google dorks when looking for OSINT (open-source intelligence) or just looking for general source
"""

# Necessary libraries
import random
import requests
from googlesearch import search
import os
import argparse
import time

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
def perform_search(query, output_file, extra_info=False):
    count = 0
    with open(output_file, 'a') as sources:
        sources.write(f"Results for query: {query}\n\n")
        try:
            for link in search(query, num_results=num_results, advanced=extra_info):
                if extra_info:
                    items = link.split(',')
                    sources.write(f'URL:{items[0]} | Title: {items[1]} | Description: {items[2]}\n')
                    count += 1
                    if args.display:
                        print(link)
                else:
                    sources.write(f'Link: {link}\n')
                    count += 1
                    if args.display:
                        print(link)
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
parser.add_argument('-df', '--dorkfile', type=str, help="Reads file with queries to run multiple queries at once", default="", required=False)

args = parser.parse_args()

# Query limit before adding buffer times between queries
# To prevent Google from shutting out 'bot' / 429 Client Error
QUERY_LIMIT = 0
query_count = 0

# Initialize variables
num_results = args.results
dork = args.query
outfile = args.output
dork_file = args.dorkfile

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
            query_count += 1
            if dork and query_count <= QUERY_LIMIT:
                if args.info:
                    try:
                        time.sleep(random.randint(0, 5))
                        validate_query(dork)
                        count = perform_search(dork, outfile, True)
                        print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    try:
                        time.sleep(random.randint(0, 5))
                        validate_query(dork)
                        count = perform_search(dork, outfile)
                        print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                    except ValueError as e:
                        print(f"Error: {e}")
            else:
                if args.info:
                    try:
                        validate_query(dork)
                        count = perform_search(dork, outfile, True)
                        print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    try:
                        validate_query(dork)
                        count = perform_search(dork, outfile)
                        print(f"\nNumber of results found for query '{dork}': {count}\n\n")
                    except ValueError as e:
                        print(f"Error: {e}")
else:
    if not dork:
        print("Error: No query provided. Use -q to specify a search query.")
        exit(1)
    count = perform_search(dork, outfile)
    print(f"\nNumber of results found for query '{dork}': {count}")

print(f"Results saved to {outfile}")


# # Download the files listed in 'sources.txt'
# with open('sources.txt', 'r') as sources:
#     for source in sources:
#         source = source.strip()
#         if source:
#             os.system(f"curl -o ~/Desktop/sources/ {source}")
