from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from crawler_service import crawl_website
from download_service import download_all_pdfs
from excel_service import create_excel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")


class UrlRequest(BaseModel):
    url: str


crawl_status = {
    "pages": 0,
    "pdf_found": 0,
    "downloaded": 0,
    "running": False
}


@app.get("/")
def home():
    return {"message": "PDF Discovery API Running"}


@app.get("/status")
def get_status():
    return crawl_status


@app.post("/crawl")
def crawl(req: UrlRequest):

    crawl_status["running"] = True
    crawl_status["pages"] = 0
    crawl_status["pdf_found"] = 0
    crawl_status["downloaded"] = 0

    pdf_links = crawl_website(req.url)

    crawl_status["pdf_found"] = len(pdf_links)

    downloaded, folder = download_all_pdfs(pdf_links, req.url)

    crawl_status["downloaded"] = len(downloaded)

    excel_file = create_excel(pdf_links, folder)

    crawl_status["running"] = False

    return {
        "pdf_found": len(pdf_links),
        "downloaded": len(downloaded),
        "folder": folder,
        "excel_file": excel_file
    }