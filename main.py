from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os

# Set up the Selenium WebDriver with WebDriver Manager
download_dir = './Downloads'

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver using Service object
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the page
url = "https://www.tsetmc.com/InstInfo/10795723506538053"
driver.get(url)

try:
    # Wait for the button to be clickable and click it
    export_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "InsExport"))
    )
    export_button.click()
    print("Clicked on the export button.")
except Exception as e:
    print("An error occurred:", e)
finally:
    # Wait for the download to complete (adjust time as needed)
    time.sleep(10)
    driver.quit()

# Identify and process the downloaded file
files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
if files:
    file_path = os.path.join(download_dir, files[0])
    try:
        df = pd.read_excel(file_path)
        print("Excel file loaded successfully!")
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print("An error occurred while reading the Excel file:", e)
else:
    print("No Excel file found in the download directory.")

