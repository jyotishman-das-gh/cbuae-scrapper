from playwright.sync_api import sync_playwright
import requests
import os
import urllib.parse
import time
import json
import boto3

# Load AWS credentials
with open("config.json") as f:
    config = json.load(f)["AWS"]

s3_client = boto3.client(
    "s3",
    aws_access_key_id=config["access_key_id"],
    aws_secret_access_key=config["secret_access_key"],
    region_name=config["region"]
)

BUCKET_NAME = config["pdf_bucket_name"]

# Category keywords for S3 subfolders
CATEGORIES = {
    "CBUAE Annual Reports": ["annual", "report"],
    "Monthly Reports": ["monthly", "monetary", "ms-"],
    "Quarterly Reports": ["q1", "q2", "q3", "q4", "quarterly"],
    "Financial Stability Report": ["stability", "fsr"],
    "UAE MSME Business Survey Report": ["msme", "survey"],
}

def sanitize_filename(name):
    return urllib.parse.unquote(name.split("/")[-1].split("?")[0])

def extract_title_and_date(filename):
    parts = filename.replace('.pdf', '').split('-')
    for i, part in enumerate(parts):
        if any(x in part.lower() for x in ["q1", "q2", "q3", "q4", "202", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]):
            date = "-".join(parts[i:])
            title = "-".join(parts[:i])
            return title.strip(), date.strip()
    return filename.replace('.pdf', ''), "undated"

def categorize_s3_folder(filename):
    name = filename.lower()
    for folder, keywords in CATEGORIES.items():
        if any(kw in name for kw in keywords):
            return folder
    return "Uncategorized"

def upload_to_s3(local_path, file_name):
    category_folder = categorize_s3_folder(file_name)
    s3_key = f"{category_folder}/{file_name}"

    try:
        s3_client.upload_file(local_path, BUCKET_NAME, s3_key)
        print(f" ↑ Uploaded to S3: {s3_key}")
    except Exception as e:
        print(f"  Failed to upload {file_name} to S3: {e}")

def download_pdf(url, folder):
    file_name = sanitize_filename(url)
    title, date = extract_title_and_date(file_name)
    unique_id = f"{title}_{date}".lower()

    already_downloaded = any(
        unique_id in f.lower().replace('.pdf', '')
        for _, _, files in os.walk(folder)
        for f in files
    )

    if already_downloaded:
        print(f"Skipped (already downloaded): {file_name}")
        return

    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file_name)

    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"  Downloaded: {file_name}")
            upload_to_s3(path, file_name)
        else:
            print(f"  Failed: {file_name} — HTTP {r.status_code}")
    except Exception as e:
        print(f"  Error downloading {file_name}: {e}")

def scrape_all_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.centralbank.ae/en/news-and-publications/publications/")
        time.sleep(5)

        for page_num in range(1, 24):  # Pages 1 to 23
            print(f"\n  Processing Page {page_num}...")

            try:
                page.wait_for_selector("a[href$='.pdf']", timeout=15000, state="attached")
                pdf_links = page.query_selector_all("a[href$='.pdf']")
                print(f"  Found {len(pdf_links)} PDFs")

                for link in pdf_links:
                    href = link.get_attribute("href")
                    if href:
                        full_url = "https://www.centralbank.ae" + href if href.startswith("/") else href
                        download_pdf(full_url, folder="downloads")

            except Exception as e:
                print(f"  Failed to extract PDFs on page {page_num}: {e}")
                break

            if page_num < 23:
                try:
                    next_btn = page.locator(f"ul.pagination >> text=\"{page_num + 1}\"").first
                    next_btn.scroll_into_view_if_needed()
                    next_btn.click()
                    print(f"  Clicked Page {page_num + 1}")
                    time.sleep(3)
                except Exception as e:
                    print(f"  Pagination click failed on page {page_num + 1}: {e}")
                    break

        browser.close()

if __name__ == "__main__":
    scrape_all_pages()
