import arxiv
import os
import re
import shutil

def slugify(text):
    return re.sub(r"[^\w\-_.]", "_", text)[:100]

def fetch_and_download_papers(query="natural language processing", max_results=3, save_dir="papers"):
    os.makedirs(save_dir, exist_ok=True)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []
    for result in search.results():
        paper_id = result.entry_id.split('/')[-1]
        safe_id = slugify(paper_id)
        title_slug = slugify(result.title)

        target_filename = f"{safe_id}_{title_slug}.pdf"
        full_path = os.path.join(save_dir, target_filename)

        if not os.path.exists(full_path):
            print(f"Downloading: {result.title}")
            try:
                temp_path = result.download_pdf(dirpath=save_dir)
                shutil.move(temp_path, full_path)  # Rename after download
            except Exception as e:
                print(f"Failed to download {result.title}: {e}")
        else:
            print(f"Already downloaded: {result.title}")

        papers.append({
            "id": paper_id,
            "title": result.title,
            "summary": result.summary,
            "pdf_url": result.pdf_url
        })

    return papers
