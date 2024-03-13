import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

orgSet = {"HİZBULLAH Terör Örgütü"}

url = "https://www.terorarananlar.pol.tr/tarananlar"
driver.get(url)
data_list = []
time.sleep(5)
try:
    accept_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "acceptcookies"))
    )
    accept_cookies_button.click()
except Exception as e:
    print("Error handling cookies popup:", str(e))
while driver.find_element(By.ID, "dahaFazlaYukleBtn").is_displayed():
    driver.find_element(By.ID, "dahaFazlaYukleBtn").click()
    time.sleep(2)

# Wait for the card containers to be present
wait = WebDriverWait(driver, 10)
card_containers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "deactivated-list-card")))
for card in card_containers:
    # Extract information from each card
    photo_url = card.find_element(By.CLASS_NAME, "deactivated-list-card-img").get_attribute("style").split("url(")[1].split(");")[
        0].strip("'")

    # Execute JavaScript to get the text content
    name = driver.execute_script("return arguments[0].querySelector('.deactivated-list-card-content h6').textContent;",
                                 card).strip() or "Name not available"
    birth_info = driver.execute_script(
        "return arguments[0].querySelector('.deactivated-list-card-content span:nth-of-type(1)').textContent;",
        card).strip() or "Birth information not available"
    organization = driver.execute_script(
        "return arguments[0].querySelector('.deactivated-list-card-content span:nth-of-type(2)').textContent;",
        card).strip() or "Organization not available"
    orgSet.add(organization)
    card_data = {
        "Name": name,
        "Birth Information": birth_info,
        "Organization": organization,
        "Photo URL": photo_url
    }
    print(orgSet)
    # Append the dictionary to the list
    data_list.append(card_data)

# Close the browser
driver.quit()

output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=2)

print(f"Data saved to {output_file}")
