import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

visited = set()
pdf_links = set()

headers = {
    "User-Agent": "Mozilla/5.0"
}


def process_page(url, domain):

    global visited, pdf_links

    try:
        res = requests.get(url, headers=headers, timeout=10)

        if "text/html" not in res.headers.get("content-type", ""):
            return []

        soup = BeautifulSoup(res.text, "html.parser")

        new_links = []

        for tag in soup.find_all("a", href=True):

            link = urljoin(url, tag["href"])

            if link.lower().endswith(".pdf"):
                pdf_links.add(link)

            elif urlparse(link).netloc == domain:
                new_links.append(link)

        return new_links

    except:
        return []


def crawl_website(start_url, max_pages=200):

    global visited, pdf_links

    visited = set()
    pdf_links = set()

    domain = urlparse(start_url).netloc

    queue = [start_url]

    with ThreadPoolExecutor(max_workers=10) as executor:

        while queue and len(visited) < max_pages:

            batch = []

            while queue and len(batch) < 10:
                url = queue.pop(0)

                if url not in visited:
                    visited.add(url)
                    batch.append(url)

            results = executor.map(lambda u: process_page(u, domain), batch)

            for new_links in results:

                for link in new_links:

                    if link not in visited:
                        queue.append(link)

    return list(pdf_links)