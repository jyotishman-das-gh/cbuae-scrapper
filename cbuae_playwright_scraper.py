# from playwright.sync_api import sync_playwright
# import requests
# import os
# import urllib.parse
# import time

# def sanitize_filename(name):
#     return urllib.parse.unquote(name.split("/")[-1].split("?")[0])

# def download_pdf(url, folder):
#     file_name = sanitize_filename(url)
#     os.makedirs(folder, exist_ok=True)
#     path = os.path.join(folder, file_name)

#     already_downloaded = any(
#         file_name in files
#         for root, _, files in os.walk("downloads")
#     )

#     if already_downloaded:
#         print(f"Skipped (already downloaded): {file_name}")
#         return

#     try:
#         r = requests.get(url)
#         if r.status_code == 200:
#             with open(path, "wb") as f:
#                 f.write(r.content)
#             print(f" Downloaded: {file_name}")
#         else:
#             print(f" Failed: {file_name} — HTTP {r.status_code}")
#     except Exception as e:
#         print(f" Error downloading {file_name}: {e}")


# def scrape_all_pages():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto("https://www.centralbank.ae/en/news-and-publications/publications/")
#         time.sleep(5)

#         for page_num in range(1, 24):  # Pages 1 to 23
#             print(f"\n Processing Page {page_num}...")

#             try:
#                 # Wait for PDF links to be present in DOM (not necessarily visible)
#                 page.wait_for_selector("a[href$='.pdf']", timeout=15000, state="attached")
#                 pdf_links = page.query_selector_all("a[href$='.pdf']")
#                 print(f" Found {len(pdf_links)} PDFs")

#                 for link in pdf_links:
#                     href = link.get_attribute("href")
#                     if href:
#                         full_url = "https://www.centralbank.ae" + href if href.startswith("/") else href
#                         download_pdf(full_url, folder="downloads")

#             except Exception as e:
#                 print(f" Failed to extract PDFs on page {page_num}: {e}")
#                 break

#             if page_num < 23:
#                 try:
#                     next_btn = page.locator(f"ul.pagination >> text=\"{page_num + 1}\"").first
#                     next_btn.scroll_into_view_if_needed()
#                     next_btn.click()
#                     print(f" Clicked Page {page_num + 1}")
#                     time.sleep(3)  # allow JS to re-render
#                 except Exception as e:
#                     print(f" Pagination click failed on page {page_num + 1}: {e}")
#                     break

#         browser.close()

# if __name__ == "__main__":
#     scrape_all_pages()

from playwright.sync_api import sync_playwright
import requests
import os
import urllib.parse
import time
import json
import boto3

# Load AWS credentials from config.json
with open("config.json") as f:
    config = json.load(f)["AWS"]

s3_client = boto3.client(
    "s3",
    aws_access_key_id=config["access_key_id"],
    aws_secret_access_key=config["secret_access_key"],
    region_name=config["region"]
)

BUCKET_NAME = config["pdf_bucket_name"]


def sanitize_filename(name):
    return urllib.parse.unquote(name.split("/")[-1].split("?")[0])


def upload_to_s3(local_path, file_name):
    try:
        s3_client.upload_file(local_path, BUCKET_NAME, file_name)
        print(f" ↑ Uploaded to S3: {file_name}")
    except Exception as e:
        print(f"  Failed to upload {file_name} to S3: {e}")


def download_pdf(url, folder):
    file_name = sanitize_filename(url)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, file_name)

    already_downloaded = any(
        file_name in files
        for root, _, files in os.walk("downloads")
    )

    if already_downloaded:
        print(f"Skipped (already downloaded): {file_name}")
        return

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
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.centralbank.ae/en/news-and-publications/publications/")
        time.sleep(5)

        for page_num in range(1, 24):  # Pages 1 to 23
            print(f"\n  Processing Page {page_num}...")

            try:
                # Wait for PDF links to be present in DOM (not necessarily visible)
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
                    print(f" ➡ Clicked Page {page_num + 1}")
                    time.sleep(3)  # allow JS to re-render
                except Exception as e:
                    print(f" ⚠ Pagination click failed on page {page_num + 1}: {e}")
                    break

        browser.close()


if __name__ == "__main__":
    scrape_all_pages()
