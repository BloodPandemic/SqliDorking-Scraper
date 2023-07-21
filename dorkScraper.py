import requests
from bs4 import BeautifulSoup
import time
import signal
import sys

def get_google_search_results(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:114.0) Gecko/20100101 Firefox/114.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    return response.text

def parse_google_search_results(html):
    soup = BeautifulSoup(html, "html.parser")
    search_results = []
    result_divs = soup.find_all("div", {"class": "tF2Cxc"})
    
    for result_div in result_divs:
        link = result_div.find("a")["href"]
        title = result_div.find("h3").get_text()
        search_results.append({"title": title, "link": link})
    
    return search_results

def exit_handler(sig, frame):
    global results
    with open(output_file, "a", encoding="utf-8") as f_out:
        for query, query_results in results.items():
            f_out.write(f"Search Results for query: {query}\n")
            for idx, result in enumerate(query_results, 1):
                f_out.write(f"{idx}. {result['title']}\n")
                f_out.write(f"   Link: {result['link']}\n")
                f_out.write("\n")
            f_out.write("\n")
    print("Exiting...")
    sys.exit(0)

if __name__ == "__main__":
    input_file = "dorks.txt" #change this to match ur dorks file
    output_file = "search_results.txt"
    results = {}

    with open(input_file, "r", encoding="utf-8") as f:
        queries = f.read().splitlines()
    
    signal.signal(signal.SIGINT, exit_handler)  
    try:
        for query in queries:
            html = get_google_search_results(query)
            if html:
                results[query] = parse_google_search_results(html)
                print(f"Search results for query '{query}' obtained.")
            time.sleep(10)  #added this for rate limiting
    except KeyboardInterrupt:
        exit_handler(None, None)
