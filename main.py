from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import pandas as pd
from io import StringIO
# Navigate to the target URL



# Set up Chrome options with performance logging
options = webdriver.ChromeOptions()

options.add_argument('--ignore-certificate-errors')
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
options.add_argument('--enable-logging')
options.add_argument('--v=1')

# Initialize WebDriver using the Service object
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.tsetmc.com/InstInfo/10795723506538053"
driver.get(url)
try:
    # Wait for the button to be clickable and click it
    export_button = WebDriverWait(driver, 9).until(
        EC.element_to_be_clickable((By.ID, "InsExport"))
    )
    export_button.click()
    print("Clicked on the export button.")
except Exception as e:
    print("An error occurred:", e)


# Wait for network activities to complete
time.sleep(20)

# Retrieve all performance logs
logs_raw = driver.get_log("performance")
logs = [json.loads(entry["message"])["message"] for entry in logs_raw]

# Filter function to find the desired network response
def log_filter(log_entry): 
    return (
        log_entry["method"] == "Network.responseReceived"
    )

print("run for loop")
# Process logs to find and print relevant data
for log in filter(log_filter, logs):
    request_id = log["params"]["requestId"]
    response_url = log["params"]["response"]["url"]
    print(response_url)
    if "ClosingPriceDailyListCSV" in response_url:
        print(f"Caught CSV response from {response_url}")
        response_body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
        csv_data = response_body['body']

        # Display CSV data and parse it using Pandas
        print("CSV Data Sample:")
        print(csv_data[:500])  # Print the first 500 characters for preview

        # Parse CSV to DataFrame
        df = pd.read_csv(StringIO(csv_data))
        print("Parsed DataFrame:")
        print(df.head())

# Close the driver
driver.quit()

