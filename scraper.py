import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

url1 = "https://en.wikipedia.org/wiki/Pittsburgh"
f1 = requests.get(url1, headers=headers, timeout = 1)
f1_soup = BeautifulSoup(f1.text, 'lxml')

content_div = f1_soup.find(class_="mw-content-ltr mw-parser-output")
for tag in content_div.find_all('sup', class_='reference'):
    tag.decompose()

for tag in content_div.find_all('span', class_='mw-editsection'):
    tag.decompose()

for tag in content_div.find_all('span', class_='mw-editsection'):
    tag.decompose()

section_ids_to_remove = ['References', 'See_also', 'Further_reading', 'External_links']

for section_id in section_ids_to_remove:
    heading_tag = content_div.find('h2', id=section_id)
    if heading_tag:
        parent_div = heading_tag.parent
        for sibling in list(parent_div.next_siblings):
            if hasattr(sibling, 'decompose'):
                sibling.decompose()
        parent_div.decompose()

clean_text = content_div.get_text(separator = '\n', strip = True)
print(clean_text)

data = {}
data[url1] = clean_text

def req(url) :
  try :
    r = requests.get(url, headers = headers, timeout = 2)
    return r.text
  except :
    return "failed"

def soup(text) :
  return BeautifulSoup(text, 'lxml')

def content(soup, id) :
  content_div = soup.find(class_ = id)
  if content_div and content_div.find_all('sup', class_ = 'reference') is not None :
    for tag in content_div.find_all('sup', class_='reference'):
        tag.decompose()
  if content_div and content_div.find_all('span', class_ = 'mw-editsection') is not None :
    for tag in content_div.find_all('span', class_='mw-editsection'):
        tag.decompose()
  return content_div

def remove(section_ids, content) :
  if content is None :
    return None
  for section_id in section_ids:
    heading_tag = content.find('h2', id=section_id)
    if heading_tag:
        parent_div = heading_tag.parent
        for sibling in list(parent_div.next_siblings):
            if hasattr(sibling, 'decompose'):  # Check if it's a tag that can be decomposed
                sibling.decompose()
        parent_div.decompose()
  return content.get_text(separator = "\n", strip = True)

URLS_TO_SCRAPE = [
    'https://en.wikipedia.org/wiki/History_of_Pittsburgh',
    'https://www.britannica.com/place/Pittsburgh',
    'https://www.cmu.edu/about/history.html'
]

soups = []
for url in URLS_TO_SCRAPE :
  soups.append(soup(req(url)))

content_div2 = content(soups[0], "mw-content-ltr mw-parser-output")

content_div2 = remove(["See_also", "References", "Bibliography", "External__links"], content_div2)

print(content_div2)

data[URLS_TO_SCRAPE[0]] = content_div2

content_div3 = soups[1].find('div', class_="page2ref-true topic-content topic-type-REGULAR")
if content_div3:
    for tag in content_div3.find_all('span'):
        tag.decompose()
    content_div3 = content_div3.get_text(separator = "\n", strip = True)
else:
    content_div3 = None
    print("Could not find a div with class 'reading-channel' in the second URL.")

data[URLS_TO_SCRAPE[1]] = None

content_div4 = soups[2].find('div', class_ = "layout-content")
content_div4 = content_div4.get_text(separator = '\n', strip = True)
data[URLS_TO_SCRAPE[2]] = content_div4

events_urls = ["https://community.pghcitypaper.com/pittsburgh/EventSearch",
               ]

BASE_URL = 'https://community.pghcitypaper.com/pittsburgh/EventSearch'

TOTAL_PAGES = 26

all_events_data = []

for page_num in range(1, TOTAL_PAGES + 1):
    current_url = f"{BASE_URL}?page={page_num}&v=d"
    print(f"Scraping page {page_num} of {TOTAL_PAGES}...")

    try:
        response = requests.get(current_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        results_container = soup.find('ul', class_="pres-EventSearchRectangle uk-list uk-list-divider uk-flex@show-grid")

        if results_container:
            all_events_data.append(results_container.get_text(separator = '\n', strip = True))
        if not results_container:
            print("  -> No events found on this page. Stopping.")
            break

    except requests.exceptions.RequestException as e:
        print(f"  [!] Could not fetch page {page_num}: {e}")
    except Exception as e:
        print(f"  [!] An error occurred while parsing page {page_num}: {e}")

print(f"\n✅ Scraping complete. Total events collected: {len(all_events_data)}")

content_div5 = "\n \n".join(all_events_data)
import re

raw_text = content_div5

cleaned_lines = []
for line in raw_text.split('\n'):
    # Strip whitespace to make matching easier
    stripped_line = line.strip()

    # Create a list of conditions for lines you want to IGNORE
    if stripped_line == "Get Tickets":
        continue # Skip this line
    if re.match(r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$', stripped_line): # Regex for phone numbers
        continue # Skip this line
    if re.match(r'^\$?\d+(\.\d{2})?.*$', stripped_line): # Basic regex for prices
        continue # Skip this line

    # If the line is not noise, keep it
    if stripped_line: # Also ignore empty lines for now
        cleaned_lines.append(stripped_line)

# Join the lines back together into a single string
content_div5 = "\n".join(cleaned_lines)
data[BASE_URL] = content_div5

