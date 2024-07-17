from pathlib import Path
import pandas as pd

# Set the application directory
app_dir = Path(__file__).parent

# Path to the Excel file
file_path = app_dir / "Translated_Negative_Reviews.xlsx"

# Load the Excel file into a pandas DataFrame
translated_negative_reviews = pd.read_excel(file_path)

# Now `translated_negative_reviews` contains the data from the Excel file
