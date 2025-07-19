# dorker.py: Your Automated Google Dorking Tool

![image]([http://googleusercontent.com/image_generation_content/8](https://github.com/CyberPanther232/dorker/blob/9eba520b465ee68e03b5485f7693e6854631fb13/Dorker_Script_Logo.png))


## Program Overview

`dorker.py` is a versatile Python script designed to **automate Google search queries**, specifically focusing on **Google dorks**. Whether you're conducting **Open-Source Intelligence (OSINT)** gathering or simply looking for general information, `dorker.py` streamlines the process of extracting relevant data from Google.

## Features

* **Automated Google Searches**: Execute single or multiple Google dork queries efficiently.

* **Flexible Output**: Save search results to a specified file, with an option to display them directly in the console.

* **Configurable Results**: Control the number of search results retrieved per query.

* **Advanced Information Extraction**: Capture detailed information like titles, descriptions, and links (when available via direct scraping or API).

* **Custom User-Agent Support**: Option to specify a custom User-Agent string for requests (use with caution).

* **Google Custom Search API Integration**: Utilize the Google Custom Search JSON API for faster, more reliable, and less rate-limited queries.

* **Dork File Support**: Process a list of dorks from a file to run multiple queries in succession.

* **Network Connectivity Check**: Ensures an active internet connection before initiating searches.

## Getting Started

### Prerequisites

Before running `dorker.py`, make sure you have the following Python libraries installed:

* `requests`

* `beautifulsoup4`

You can install them using pip:

```bash
pip install requests beautifulsoup4
Google Custom Search API (Optional but Recommended)
For more robust and efficient querying, especially for advanced information extraction or frequent use, it's highly recommended to use the Google Custom Search API.

Enable the Custom Search API: Visit the Google Cloud Console and enable the "Custom Search API" for your project.

Create API Key: Go to Credentials and create an API Key.

Create a Custom Search Engine: Visit the Custom Search Engine page, create a new search engine, and configure it to search the entire web or specific sites. Note down your Search Engine ID (CX).

Usage
dorker.py can be run from the command line with various arguments.

Bash

python dorker.py -h
Command-Line Arguments
-r or --results: Sets the maximum number of results to retrieve (default: 15).

-q or --query: Specifies a single Google search query or dork query.

-o or --output: Sets the name of the output file (default: sources.txt).

-d or --display: Displays/prints the URLs or advanced information from the query results to the console.

-i or --info: Gathers advanced information such as title, description, and full URL (requires API if scraping).

-df or --dork-file: Reads a file containing multiple queries to run them in bulk.

-u or --user-agent: Allows setting a custom User-Agent string header for requests (use with caution).

-a or --api-key: Sets your Google Custom Search JSON API key.

-seid or --search-engine-id: Sets your Custom Search Engine ID (CX).

Examples
Basic Search
To perform a simple search and save results to sources.txt:

Bash

python dorker.py -q "inurl:admin login"
Display Results to Console
To display results directly in the terminal:

Bash

python dorker.py -q "site:example.com intitle:index.of" -d
Advanced Information (using API)
To get detailed results (title, description, link) using your Google Custom Search API:

Bash

python dorker.py -q "site:github.com intext:password" -i -a YOUR_API_KEY -seid YOUR_SEARCH_ENGINE_ID
Running Multiple Dorks from a File
Create a file named dorks.txt (or any other name) with one dork per line:

inurl:wp-admin
intitle:"index of" site:example.com
"confidential" filetype:pdf
Then run dorker.py with the -df option:

Bash

python dorker.py -df dorks.txt -o my_dork_results.txt
Custom User-Agent
Bash

python dorker.py -q "latest security vulnerabilities" -u "MyCustomBrowser/1.0"
Important Notes
Respect Rate Limits: When using the direct Google search (non-API), be mindful of Google's rate limits. Excessive requests can lead to temporary IP blocking. The script includes a random time.sleep to help mitigate this, especially when processing dork files.

API Usage: Using the Google Custom Search API is generally more reliable and avoids direct scraping issues, but it has daily query limits depending on your Google Cloud project's configuration.

--info Flag: When using the --info flag without an API key, the script attempts to scrape more detailed information, which might be less reliable due to changes in Google's HTML structure. For consistent advanced information, the API is recommended.

Contribution
Feel free to fork this repository, open issues, or submit pull requests. Contributions are welcome!

DISCLAIMER: This script is a proof-of-concept tool intended for ethical, informational, and authorized use only! Any illegal or unethical usage of this script is prohibited and the you will be responsible for any misuse of this script!
