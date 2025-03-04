import requests
from bs4 import BeautifulSoup
from googlesearch import search

response = requests.get("https://phasmophobia.fandom.com/wiki/Ghost")
# https://www.whitehousehistory.org/the-presidents-timeline
print(response.status_code)
response.encoding = "utf-8"

# with open("list.html", "w", encoding="utf-8") as file:
    # file.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify)

"""table = soup.find("table")
rows = table.find_all("tr")

headers = [header.text.strip() for header in rows[0].find_all("th")]

entries = []
for row in rows[1:]:
    cells = row.find_all("td")
    entry = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
    entries.append(entry)

# generate markdown file
with open("list.md", "w") as list_file:
    list_file.write("| " + " | ".join(headers) + " |\n")
    list_file.write("|" + " --- |" * len(headers) + "\n")
    for entry in entries:
        list_file.write("| " + " | ".join(entry.values()) + " |\n")"""

table = soup.find_all("table")

TABLE_NO = 1
rows = table[TABLE_NO].find_all("tr")


headers = [header.text.strip() for header in rows[0].find_all("th")]
headers.append('Link to google search results')

# print(headers)
# quit()

N_COLUMNS = 4

tags = ["td", "th"]

entries = []
for row in rows[1:]:
    cells = row.find_all(tags)
    entry = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
    entry[headers[N_COLUMNS - 1]] = "[Link to search results](" + entry[headers[0]].replace(" ", "_") + ".html)"
    entries.append(entry)

with open("list.md", "w", encoding="utf-8") as file:
    file.write("# List of ghost types; source: [phasmophobia.fandom.com](phasmophobia.fandom.com)\n")
    file.write("| " + " | ".join(headers) + " |\n")
    file.write("|" + " --- |" * len(headers) + "\n")
    for entry in entries:
        file.write("| " + " | ".join(entry.values()) + " |\n")

for entry in entries:
    search_res = search(entry[headers[0]] + " phasmo", stop=1)
    processed_ghost_type = entry[headers[0]].replace(" ", "_")
    with open(processed_ghost_type + ".md", "w", encoding = "utf-8") as file:
        url_dummy_list = list(search_res)
        url = url_dummy_list[0]
        print(url)
        subpage_request = requests.get(url)
        subpage_request.encoding = "utf-8"
        subpage_soup = BeautifulSoup(subpage_request.text, "html.parser")
        file.write("# Google search results for " + entry[headers[0]] + "\n")
        file.write("## " + entry[headers[0]] + "; info taken from: " + url + "\n")
        file.write("### Journal entry:\n")
        occurrences = subpage_soup.find_all("p")
        file.write("*" + occurrences[1].text.strip() + "*\n")
        file.write("\n### Short description:\n")
        file.write(occurrences[2].text.strip())




# PRESIDENTS_LIST = 9


# items = [li.text.strip() for li in lists[PRESIDENTS_LIST].find_all("li")] 1517

# print(items)

# content = "\n".join([f"- {item}" for item in items])

# with open("list.md", "w", encoding="utf-8") as file:
    # file.write(content)

