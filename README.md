# CBUAE Scraper

This repository contains a fully automated PDF scraper for the **Central Bank of the UAE (CBUAE)** publications site.

It extracts documents from the [CBUAE Publications](https://www.centralbank.ae/en/news-and-publications/publications/) page, organizes them by category, and uploads new documents daily to an AWS S3 bucket.

---

## Features

- Scrapes all PDF publications from all 23 paginated pages on the CBUAE site.
- Handles dynamic loading using **Playwright** (headless browser automation).
- Categorizes downloaded files into subfolders such as:
  - CBUAE Annual Reports
  - Monthly Reports
  - Quarterly Reports
  - Financial Stability Report
  - UAE MSME Business Survey Report
  - Uncategorized (fallback)
- Uploads newly downloaded PDFs to a specified **AWS S3 Bucket**
- Keeps track of already downloaded files to avoid duplication.
- Daily automation via **Windows Task Scheduler** at 3:00 PM.

---

## Folder Structure

```
cbuae_scraper/
├── downloads/                    # Contains categorized downloaded PDFs
├── venv/                         # Virtual environment (ignored in repo)
├── auto_runner.py                # Scheduler script to auto-launch the scraper
├── cbuae_playwright_scraper.py  # Main scraping logic using Playwright
├── config.json                   # Removed from repo (contains secrets)
├── organize_pdfs.py              # Optional categorization script
├── requirements.txt              # Python dependencies
```

---

## AWS S3 Integration

- Credentials are read from `config.local.json` (excluded from Git using `.gitignore`).
- Required fields in `config.local.json`:

```json
{
  "AWS": {
    "access_key_id": "<YOUR_AWS_ACCESS_KEY_ID>",
    "secret_access_key": "<YOUR_AWS_SECRET_ACCESS_KEY>",
    "pdf_bucket_name": "<S3_BUCKET_NAME>",
    "region": "<AWS_REGION>"
  }
}
```

---

## Automation

- The scraper is scheduled to run daily at 3:00 PM via Windows Task Scheduler.
- It calls `python auto_runner.py` which internally runs the scraper script.

---

## Requirements

Install required packages inside a virtual environment:

```bash
pip install -r requirements.txt
```

To install Playwright browsers (mandatory):

```bash
playwright install
```

---

## Setup

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies and run `playwright install`.
4. Set up AWS credentials in `config.local.json`.
5. (Optional) Run `organize_pdfs.py` to re-categorize files.
6. Use `auto_runner.py` to test scheduled runs.

---

## Task Scheduler Setup

To enable real automation (runs even when VS Code is closed):

1. Open Windows Task Scheduler.
2. Create a new Basic Task.
3. Trigger: Daily at 3:00 PM.
4. Action: Start a program.
5. Browse and select:
```
Program/script: C:\path\to\venv\Scripts\python.exe
Add arguments: auto_runner.py
Start in: D:\path\to\cbuae_scraper
```
6. Save.

---

## Notes

- Playwright was chosen over Selenium because the CBUAE website heavily uses JavaScript. Selenium was unable to reliably navigate all paginated content or apply filters.
- The S3 bucket remains empty if CBUAE doesn’t publish anything new. Duplicates are skipped based on filename checks.
- `.gitignore` ensures that sensitive credentials and large files (like `venv`) are excluded.

---

## License

[Add your license information here]
