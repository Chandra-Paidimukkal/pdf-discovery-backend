import os
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

from registry_service import file_exists, register_file

BASE_DIR = "downloads"

os.makedirs(BASE_DIR, exist_ok=True)


def get_folder_name(url):

    domain = urlparse(url).netloc
    parts = domain.split(".")

    name = parts[1] if parts[0] == "www" else parts[0]

    base_path = os.path.join(BASE_DIR, name)

    if not os.path.exists(base_path):
        return base_path

    i = 1

    while True:

        new_path = os.path.join(BASE_DIR, f"{name}_{i}")

        if not os.path.exists(new_path):
            return new_path

        i += 1


def download_single(link, folder):

    if file_exists(link):
        return None

    try:

        filename = link.split("/")[-1]

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        path = os.path.join(folder, filename)

        r = requests.get(link, timeout=20)

        with open(path, "wb") as f:
            f.write(r.content)

        register_file(link)

        return path

    except:
        return None


def download_all_pdfs(pdf_links, start_url):

    folder = get_folder_name(start_url)

    os.makedirs(folder, exist_ok=True)

    downloaded = []

    with ThreadPoolExecutor(max_workers=8) as executor:

        results = executor.map(lambda link: download_single(link, folder), pdf_links)

    for r in results:
        if r:
            downloaded.append(r)

    return downloaded, folder