import os
import shutil

SOURCE_FOLDER = "downloads"

# Folder name to keywords mapping
CATEGORIES = {
    "CBUAE Annual Reports": ["annual", "report"],
    "Monthly Reports": ["monthly", "monetary", "ms-"],
    "Quarterly Reports": ["q1", "q2", "q3", "q4", "quarterly"],
    "Financial Stability Report": ["stability", "fsr"],
    "UAE MSME Business Survey Report": ["msme", "survey"],
}

def categorize(filename):
    name = filename.lower()
    for folder, keywords in CATEGORIES.items():
        if any(kw in name for kw in keywords):
            return folder
    return "Uncategorized"

def organize_pdfs():
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.endswith(".pdf"):
            category = categorize(filename)
            target_folder = os.path.join(SOURCE_FOLDER, category)
            os.makedirs(target_folder, exist_ok=True)

            src_path = os.path.join(SOURCE_FOLDER, filename)
            dst_path = os.path.join(target_folder, filename)

            # Only move if not already moved
            if not os.path.exists(dst_path):
                shutil.move(src_path, dst_path)
                print(f"Moved {filename} → {category}/")
            else:
                print(f"Already in place: {filename}")

if __name__ == "__main__":
    organize_pdfs()
