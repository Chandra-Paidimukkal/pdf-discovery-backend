# PDF Discovery Platform — Stage 1

> **Agentic Document Extraction System · Stage 1: Discovery & Dataset Generation**

A production-ready platform to crawl websites, discover PDF documents, download them locally, and generate formatted Excel datasets.

---

## Architecture Overview

```
project_pdf_downloader/
├── backend/                   # FastAPI Python backend
│   ├── api/
│   │   └── server.py          # REST API endpoints
│   ├── services/
│   │   ├── crawler_service.py   # BFS website crawler
│   │   ├── discovery_service.py # PDF link detection
│   │   ├── download_service.py  # PDF downloader
│   │   ├── excel_service.py     # Excel generation (Pandas + OpenPyXL)
│   │   └── registry_service.py  # JSON document registry
│   ├── models/
│   │   └── document_model.py    # Pydantic request/response models
│   ├── utils/
│   │   ├── url_utils.py         # URL normalization & helpers
│   │   └── logger.py            # Structured logging
│   ├── main.py                  # Entry point (uvicorn)
│   └── requirements.txt
│
├── frontend/
│   ├── index.html               # Standalone React app (CDN, no npm needed)
│   ├── src/
│   │   ├── components/
│   │   │   ├── UrlInput.jsx     # URL input component
│   │   │   ├── PdfList.jsx      # PDF results table
│   │   │   └── DownloadButton.jsx
│   │   ├── pages/
│   │   │   └── HomePage.jsx     # Main page
│   │   └── services/
│   │       └── api.js           # API client
│   └── package.json
│
├── data/
│   ├── downloads/               # Downloaded PDFs (organized by domain)
│   ├── excel/                   # Generated Excel files
│   └── registry/
│       └── documents.json       # Download registry
│
├── start_backend.sh
├── start_frontend.sh
└── README.md
```

---

## Quick Start

### 1. Start the Backend

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Start the API server
python main.py
# → http://localhost:8000
# → API docs: http://localhost:8000/docs
```

### 2. Start the Frontend

**Option A — Standalone HTML (no npm required):**
```bash
cd frontend
python3 -m http.server 3000
# → http://localhost:3000
```

**Option B — React development server:**
```bash
cd frontend
npm install
npm start
# → http://localhost:3000
```

---

## API Reference

### POST /crawl
Crawl a website and discover all PDF links.

**Request:**
```json
{ "url": "https://example.com" }
```

**Response:**
```json
{
  "pdf_links": ["https://example.com/file.pdf"],
  "total_found": 1,
  "pages_crawled": 5
}
```

---

### POST /download
Download a single PDF to local storage.

**Request:**
```json
{ "url": "https://example.com/file.pdf" }
```

**Response:**
```json
{
  "status": "downloaded",
  "path": "data/downloads/example.com/file.pdf",
  "filename": "file.pdf",
  "size_bytes": 204800,
  "already_existed": false
}
```

---

### POST /generate-excel
Generate a formatted Excel dataset from a list of PDF URLs.

**Request:**
```json
{
  "pdf_links": [
    "https://example.com/file1.pdf",
    "https://example.com/file2.pdf"
  ]
}
```

**Response:**
```json
{
  "excel_path": "data/excel/pdf_links_20260309_120000.xlsx",
  "total_pdfs": 2,
  "filename": "pdf_links_20260309_120000.xlsx"
}
```

---

### GET /download-excel/{filename}
Download the generated Excel file.

---

### GET /documents
List all registered downloaded documents.

---

## Excel Output Format

The generated Excel file contains:

| Column        | Description                        |
|---------------|------------------------------------|
| PDF Name      | Filename extracted from URL        |
| PDF URL       | Full URL of the PDF                |
| Domain        | Source domain                      |
| Discovered At | Timestamp                          |

Features:
- Dark header row with white text
- Alternating row colors
- Auto-adjusted column widths
- Frozen top row
- AutoFilter enabled

---

## Document Registry

Downloaded documents are logged to `data/registry/documents.json`:

```json
[
  {
    "file": "data/downloads/example.com/report.pdf",
    "url": "https://example.com/report.pdf",
    "filename": "report.pdf",
    "domain": "example.com",
    "size_bytes": 204800,
    "timestamp": "2026-03-09 12:00:00"
  }
]
```

---

## Technology Stack

**Backend:** Python · FastAPI · BeautifulSoup4 · Pandas · OpenPyXL · Pydantic  
**Frontend:** React 18 · TailwindCSS · Space Mono · DM Sans

---

## Stage 2 Extensions (Planned)

This architecture is designed to extend into:

- 🤖 AI document extraction (schema-driven field extraction)
- 📊 Structured dataset generation from PDF content
- 🔍 Vector search across document collection
- ✅ Document approval workflows
- 🗂️ Multi-source crawling and deduplication
- 📤 Export to multiple formats (CSV, JSON, Parquet)
