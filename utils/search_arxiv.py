import os
import re
import requests
from bs4 import BeautifulSoup

ARXIV_API_URL = "http://export.arxiv.org/api/query"

# Function to sanitize filenames (remove invalid Windows characters)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def search_arxiv(query, max_results=5, download_dir="papers"):
    os.makedirs(download_dir, exist_ok=True)

    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    response = requests.get(ARXIV_API_URL, params=params)
    soup = BeautifulSoup(response.content, features="xml")

    entries = soup.find_all("entry")
    downloaded = []

    for entry in entries:
        paper_id = entry.id.text.split('/')[-1]
        title = entry.title.text.strip().replace("\n", " ")
        pdf_url = f"http://arxiv.org/pdf/{paper_id}"

        # Sanitize the title to make it safe for filenames
        safe_title = sanitize_filename(title)
        filename = f"{paper_id}_{safe_title.replace(' ', '_')}.pdf"
        save_path = os.path.join(download_dir, filename)

        if not os.path.exists(save_path):
            print(f"Downloading: {title}")
            pdf_data = requests.get(pdf_url)
            if pdf_data.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(pdf_data.content)
            else:
                print(f"❌ Failed to download {pdf_url}")
                continue
        else:
            print(f"Already downloaded: {title}")

        downloaded.append((save_path, paper_id, title))

    print(f"[DEBUG] downloaded_papers: {downloaded}")
    return downloaded
