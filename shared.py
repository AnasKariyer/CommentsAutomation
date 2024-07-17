from pathlib import Path
import pandas as pd

# Define the path to the Excel file
app_dir = Path(__file__).parent
file_path = app_dir / "Translated_Negative_Reviews.xlsx"

# Check if the file exists
if not file_path.is_file():
    raise FileNotFoundError(f"File not found: {file_path}. Please ensure the file is located in the same directory as this script.")

# Read the Excel file into a pandas DataFrame
negative_reviews = pd.read_excel(file_path)

# Define the mappings for categories and languages
category_language_mapping = {
    "User Interface Issues": {
        "TR": "Kullanıcı Arayüzü Sorunları (TR)",
        "EN": "User Interface Issues (EN)"
    },
    "Performance Problems": {
        "TR": "Performans Sorunları (TR)",
        "EN": "Performance Problems (EN)"
    },
    "Job Search Functionality": {
        "TR": "İş Arama İşlevselliği (TR)",
        "EN": "Job Search Functionality (EN)"
    },
    "Notification Issues": {
        "TR": "Bildirim Sorunları (TR)",
        "EN": "Notification Issues (EN)"
    },
    "Application Process": {
        "TR": "Başvuru Süreci (TR)",
        "EN": "Application Process (EN)"
    },
    "Profile Management": {
        "TR": "Profil Yönetimi (TR)",
        "EN": "Profile Management (EN)"
    },
    "Customer Support": {
        "TR": "Müşteri Desteği (TR)",
        "EN": "Customer Support (EN)"
    },
    "Account Management": {
        "TR": "Hesap Yönetimi (TR)",
        "EN": "Account Management (EN)"
    }
}

# Flatten the mapping for easier access
flattened_mapping = {v[lang]: k for k, v in category_language_mapping.items() for lang in v}
