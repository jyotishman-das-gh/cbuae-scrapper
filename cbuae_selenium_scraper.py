# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time
# import requests
# import os

# # Setup Chrome
# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# service = Service(executable_path="./chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Open the Publications page
# url = "https://www.centralbank.ae/en/news-and-publications/publications/"
# driver.get(url)
# time.sleep(3)  # let initial content load

# # Scroll to load more (infinite scroll style)
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)  # wait for new content
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

# # Create downloads folder
# if not os.path.exists("downloads"):
#     os.makedirs("downloads")

# # Find all PDF links
# pdf_links = driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf")]')
# print(f"Found {len(pdf_links)} PDFs")

# # Download each PDF
# for i, link in enumerate(pdf_links, start=1):
#     pdf_url = link.get_attribute("href")
#     file_name = pdf_url.split("/")[-1].split("?")[0]
#     file_path = os.path.join("downloads", file_name)

#     try:
#         response = requests.get(pdf_url)
#         with open(file_path, "wb") as f:
#             f.write(response.content)
#         print(f"[{i}] Downloaded: {file_name}")
#     except Exception as e:
#         print(f"❌ Failed to download {pdf_url}: {e}")

# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time
# import requests
# import os

# # Setup Chrome
# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# service = Service(executable_path="./chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Open the Publications page
# url = "https://www.centralbank.ae/en/news-and-publications/publications/"
# driver.get(url)
# time.sleep(3)  # allow initial load

# # Create downloads folder if not exists
# if not os.path.exists("downloads"):
#     os.makedirs("downloads")

# # Get already downloaded filenames
# downloaded_files = set(os.listdir("downloads"))

# # Loop through all 23 pages
# for page in range(1, 24):
#     print(f"\n Processing Page {page}...")

#     # Wait for page content
#     time.sleep(3)

#     # Find all PDF download links on current page
#     pdf_links = driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf")]')
#     print(f" Found {len(pdf_links)} PDFs on page {page}")

#     # Download new PDFs
#     for i, link in enumerate(pdf_links, start=1):
#         pdf_url = link.get_attribute("href")
#         if not pdf_url:
#             continue
#         file_name = pdf_url.split("/")[-1].split("?")[0]
#         file_path = os.path.join("downloads", file_name)

#         if file_name in downloaded_files:
#             print(f"[{i}] Skipped (already downloaded): {file_name}")
#             continue

#         try:
#             response = requests.get(pdf_url)
#             with open(file_path, "wb") as f:
#                 f.write(response.content)
#             print(f"[{i}]  Downloaded: {file_name}")
#             downloaded_files.add(file_name)  # Add to the set
#         except Exception as e:
#             print(f" Failed to download {pdf_url}: {e}")

#     # Go to the next page using pagination button (if not last page)
#     # Go to the next page using pagination number (if not last page)
#     # Go to the next page using dynamic <li>/<a>/<span> structure
#     if page < 23:
#         try:
#             next_page = page + 1
#             xpath = f'//ul[contains(@class,"pagination")]/li/a[span[text()="{next_page}"]]'
#             next_button = driver.find_element(By.XPATH, xpath)
#             driver.execute_script("arguments[0].click();", next_button)
#             print(f" Moving to Page {next_page}...")
#             time.sleep(2)  # wait for content to update
#         except NoSuchElementException:
#             print(f" Pagination button for Page {next_page} not found. Exiting.")
#             break


# driver.quit()
# print("\n All pages processed. Script complete.")

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import requests
# import os

# # Setup Chrome
# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# # Add headless option for production use
# # chrome_options.add_argument("--headless")
# service = Service(executable_path="./chromedriver.exe")
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Open the Publications page
# url = "https://www.centralbank.ae/en/news-and-publications/publications/"
# driver.get(url)
# time.sleep(3)

# # Create downloads folder if not exists
# if not os.path.exists("downloads"):
#     os.makedirs("downloads")

# # Track downloaded files
# downloaded_files = set(os.listdir("downloads"))
# total_downloaded = 0
# total_pdfs_found = 0

# # Function to download PDFs on current page
# def download_pdfs_on_page(page_num):
#     global total_downloaded, total_pdfs_found
    
#     print(f"\n🔄 Processing Page {page_num}...")
#     time.sleep(2)
    
#     # Wait for page to load completely
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, '//a[contains(@href, ".pdf")]'))
#     )
    
#     # Get all PDF links on the current page
#     pdf_links = driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf")]')
#     print(f"📄 Found {len(pdf_links)} PDFs on page {page_num}")
#     total_pdfs_found += len(pdf_links)
    
#     for i, link in enumerate(pdf_links, start=1):
#         try:
#             pdf_url = link.get_attribute("href")
#             if not pdf_url:
#                 continue
#             file_name = pdf_url.split("/")[-1].split("?")[0]
#             file_path = os.path.join("downloads", file_name)
            
#             if file_name in downloaded_files:
#                 print(f"[{i}] Skipped (already downloaded): {file_name}")
#                 continue
            
#             try:
#                 response = requests.get(pdf_url)
#                 with open(file_path, "wb") as f:
#                     f.write(response.content)
#                 print(f"[{i}] ✅ Downloaded: {file_name}")
#                 downloaded_files.add(file_name)
#                 total_downloaded += 1
#             except Exception as e:
#                 print(f"❌ Error downloading {pdf_url}: {e}")
#         except StaleElementReferenceException:
#             print(f"Element reference became stale for item {i}, skipping.")

# # Maximum page number (we're aiming for 23 pages)
# max_pages = 23
# current_page = 1

# try:
#     # Process first page
#     download_pdfs_on_page(current_page)
    
#     # Loop through other pages
#     while current_page < max_pages:
#         try:
#             # Find the appropriate page button
#             # Look for the next page number
#             next_page_num = current_page + 1
            
#             # Using a more robust selector for page navigation
#             # Look for the link with text matching the next page number
#             next_page_xpath = f"//div[contains(@class, 'pagination')]/a[text()='{next_page_num}']"
            
#             # Wait for the pagination element to be present
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'pagination')]"))
#             )
            
#             # Try to find the next page button
#             try:
#                 next_button = driver.find_element(By.XPATH, next_page_xpath)
#                 driver.execute_script("arguments[0].click();", next_button)
#                 print(f"➡️ Moving to Page {next_page_num}...")
#                 current_page = next_page_num
                
#                 # Wait for the page to load
#                 time.sleep(3)
                
#                 # Download PDFs from this page
#                 download_pdfs_on_page(current_page)
                
#             except NoSuchElementException:
#                 # If we can't find the exact page number, try the "Next" button
#                 try:
#                     next_button = driver.find_element(By.XPATH, "//div[contains(@class, 'pagination')]/a[contains(@class, 'next')]")
#                     driver.execute_script("arguments[0].click();", next_button)
#                     print(f"➡️ Moving to Next Page using 'Next' button...")
#                     current_page += 1
                    
#                     # Wait for the page to load
#                     time.sleep(3)
                    
#                     # Download PDFs from this page
#                     download_pdfs_on_page(current_page)
                    
#                 except NoSuchElementException:
#                     # Based on the screenshot, let's try finding the next button by its arrow symbol
#                     try:
#                         # Look for the right arrow in the pagination
#                         next_arrow = driver.find_element(By.XPATH, "//div[contains(@class, 'pagination')]//a[contains(text(), '→') or contains(@class, 'next')]")
#                         driver.execute_script("arguments[0].click();", next_arrow)
#                         print(f"➡️ Moving to Next Page using arrow button...")
#                         current_page += 1
                        
#                         # Wait for the page to load
#                         time.sleep(3)
                        
#                         # Download PDFs from this page
#                         download_pdfs_on_page(current_page)
                        
#                     except NoSuchElementException:
#                         print(f"❌ Could not find any 'Next' button or page {next_page_num} button. Trying one more approach...")
                        
#                         # One last attempt - try to find any page navigation element
#                         try:
#                             # From the screenshot, I can see the navigation has page numbers in a row
#                             all_page_links = driver.find_elements(By.XPATH, "//div[contains(@class, 'pagination')]/a")
                            
#                             # If we found page links, click the one after the current
#                             next_link_found = False
#                             for link in all_page_links:
#                                 try:
#                                     link_text = link.text.strip()
#                                     if link_text.isdigit() and int(link_text) > current_page:
#                                         driver.execute_script("arguments[0].click();", link)
#                                         print(f"➡️ Moving to Page {link_text} from pagination list...")
#                                         current_page = int(link_text)
#                                         next_link_found = True
                                        
#                                         # Wait for page to load
#                                         time.sleep(3)
                                        
#                                         # Download PDFs from this page
#                                         download_pdfs_on_page(current_page)
#                                         break
#                                 except:
#                                     continue
                            
#                             if not next_link_found:
#                                 print("❌ No suitable next page link found in pagination. Ending scrape.")
#                                 break
                                
#                         except NoSuchElementException:
#                             print("❌ Could not find pagination elements at all. Ending scrape.")
#                             break
                    
#         except Exception as e:
#             print(f"❌ Error navigating to next page: {e}")
#             break

# except Exception as e:
#     print(f"❌ Unexpected error: {e}")

# finally:
#     # Close the browser
#     driver.quit()
#     print(f"\n✅ Scraping complete. Found {total_pdfs_found} PDFs in total, downloaded {total_downloaded} new files.")
#     print(f"📁 All files saved to the 'downloads' folder.")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import urllib.parse

# Setup Chrome
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path="./chromedriver.exe")
    return webdriver.Chrome(service=service, options=chrome_options)

# Filters to loop through
filters = {
    "Annual Reports": "CBUAE Annual Reports",
    "Monthly Reports": "Monthly Reports",
    "Quarterly Reports": "Quarterly Reports",
    "Stability Reports": "Financial Stability Report",
    "MSME Reports": "UAE MSME Business Survey Report"
}

base_url = "https://www.centralbank.ae/en/news-and-publications/publications/"

def sanitize_filename(name):
    return urllib.parse.unquote(name.split("/")[-1].split("?")[0])

# Track all downloaded files globally
downloaded_files = set()

def download_pdfs_on_page(driver, folder, page_number):
    print(f"\n🔄 Processing Page {page_number}...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, ".pdf")]'))
        )
    except TimeoutException:
        print(" Timeout waiting for PDF links.")
        return

    download_buttons = driver.find_elements(By.XPATH, '//a[contains(@class, "download")]')
    pdf_links = download_buttons or driver.find_elements(By.XPATH, '//a[contains(@href, ".pdf")]')

    print(f" Found {len(pdf_links)} PDFs on page {page_number}")

    os.makedirs(folder, exist_ok=True)

    for i, link in enumerate(pdf_links, start=1):
        try:
            pdf_url = link.get_attribute("href")
            if not pdf_url or not pdf_url.endswith(".pdf"):
                continue

            file_name = sanitize_filename(pdf_url)
            file_path = os.path.join(folder, file_name)

            if file_name in downloaded_files:
                print(f"[{i}] Skipped (already downloaded): {file_name}")
                continue

            response = requests.get(pdf_url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"[{i}]  Downloaded: {file_name}")
                downloaded_files.add(file_name)
            else:
                print(f" Failed to download {file_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f" Error downloading file {i}: {e}")

def get_total_pages(driver):
    try:
        spans = driver.find_elements(By.XPATH, "//ul[contains(@class, 'pagination')]//a/span")
        page_numbers = [int(span.text) for span in spans if span.text.isdigit()]
        return max(page_numbers) if page_numbers else 1
    except:
        return 1

def process_filter_section(driver, filter_label, folder_prefix):
    print(f"\n Processing Filter: {filter_label}")

    driver.get(base_url)
    time.sleep(5)

    # Click the filter label directly
    try:
        label_xpath = f"//label[contains(normalize-space(), '{filter_label}')]"
        label = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, label_xpath))
        )
        driver.execute_script("arguments[0].click();", label)
        time.sleep(3)
    except Exception as e:
        print(f" Could not apply filter '{filter_label}': {e}")
        return

    total_pages = get_total_pages(driver)
    print(f" Total pages in '{filter_label}': {total_pages}")

    for page in range(1, total_pages + 1):
        download_pdfs_on_page(driver, f"downloads/{folder_prefix}", page)

        if page < total_pages:
            try:
                old_page_source = driver.page_source
                page_xpath = f"//ul[contains(@class, 'pagination')]//a[span[text()='{page + 1}']]"
                next_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, page_xpath))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                time.sleep(1)
                next_btn.click()

                # Wait for content to change
                WebDriverWait(driver, 10).until(
                    lambda d: d.page_source != old_page_source
                )

                time.sleep(2)
            except Exception as e:
                print(f" Could not go to page {page + 1}: {e}")
                break

if __name__ == "__main__":
    driver = init_driver()
    try:
        for folder, label in filters.items():
            process_filter_section(driver, label, folder)
    finally:
        driver.quit()
        print("\n Scraping complete.")


