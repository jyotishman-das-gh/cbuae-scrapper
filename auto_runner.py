import schedule
import time
import os

def run_scraper():
    print(" Running scheduled scraper...")
    os.system("python cbuae_playwright_scraper.py")

schedule.every().day.at("15:00").do(run_scraper)

print(" Scheduler is running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)
