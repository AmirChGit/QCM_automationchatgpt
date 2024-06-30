#"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\path\to\your\chrome\profile"

import os
import time
import json
import pyperclip
import pandas as pd
import random
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the Excel file containing the subjects
excel_path = "C:/Users/achachoui/Documents/repository/QCM_automationchatgpt/Subjects/Subjects.xlsx"
last_processed_subject_file = "C:/Users/achachoui/Documents/repository/QCM_automationchatgpt/last_Maths_subject.txt"
chatgpt_chat_link = "https://chatgpt.com/c/28cb7862-3ed1-4c81-a0e0-4c7764d88808"
json_output_path = "C:/Users/achachoui/Documents/repository/QCM_automationchatgpt/Milestone1_Part2"

# Read subjects from the first column of the Excel file
df = pd.read_excel(excel_path)
subjects = df.iloc[:, 0].dropna().tolist()

# Define element selectors
selectors = {
    "textarea": 'div.flex.min-w-0.flex-1.flex-col textarea#prompt-textarea',
    "send_button": 'div.flex.items-end.gap-1\\.5.md\\:gap-2 > button:nth-child(3)',
    "response_div": 'div.markdown.prose.w-full.break-words.dark\\:prose-invert.dark',
    "continue_button": '.btn.relative.btn-secondary.whitespace-nowrap.border-0.md\\:border',
    "regenerate_button": '.btn.relative.btn-primary.m-auto',
    "gpt4_limit_div": 'div.font-bold.text-token-text-primary'
}

# Function to read the last processed subject
def read_last_processed_subject():
    if os.path.exists(last_processed_subject_file):
        with open(last_processed_subject_file, 'r') as file:
            content = file.read().strip()
            if content:
                return content
    return None

# Function to save the last processed subject
def save_last_processed_subject(subject):
    with open(last_processed_subject_file, 'w') as file:
        file.write(subject)

# Function to generate a unique 6-digit ID
def generate_unique_id():
    return str(random.randint(100000, 999999))

# Set up the Selenium WebDriver to connect to the existing Chrome session
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

# Function to scroll to the top of the page
def scroll_to_top():
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)  # Wait for 2 seconds to ensure the page has scrolled

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for 2 seconds to ensure the page has scrolled

# Function to check for GPT-4 limit and handle accordingly
def check_gpt4_limit():
    try:
        limit_divs = driver.find_elements(By.CSS_SELECTOR, selectors["gpt4_limit_div"])
        for limit_div in limit_divs:
            if "You’ve reached your GPT-4o limit." in limit_div.text:
                print("Reached GPT-4 limit. Waiting for 1 hour.")
                time.sleep(3600)  # Wait for 1 hour
                driver.refresh()
                time.sleep(5)
                return True
    except Exception as e:
        print("GPT-4 limit not reached.")
    return False

# Function to reset the chat history using pyautogui actions
def reset_chat_history_with_pyautogui():
    print("Resetting chat history with pyautogui...")
    driver.refresh()
    time.sleep(5)  # Wait for the page to reload
    
    # Perform the first moveTo and click action
    # print(pyautogui.position())
    pyautogui.moveTo(1910, 106)
    pyautogui.mouseDown(button='left')
    time.sleep(18)
    pyautogui.mouseUp(button='left')

    pyautogui.moveTo(772, 185)
    pyautogui.click()
    pyautogui.moveTo(1910, 935)

    for variable in range(31):
        pyautogui.click()

    pyautogui.moveTo(199, 111)
    pyautogui.click()

    pyautogui.moveTo(320, 206)
    pyautogui.click()
    
    pyautogui.moveTo(1289, 744)
    pyautogui.click()
    
    time.sleep(20)  # Wait for 20 seconds to ensure actions complete

# Function to click the "Continue generating" button if found
def click_continue_generating():
    scroll_to_bottom()
    try:
        continue_button = driver.find_element(By.CSS_SELECTOR, selectors["continue_button"])
        continue_button.click()
        print("Clicked 'Continue generating' button.")
        return True
    except Exception as e:
        print("No 'Continue generating' button found.")
        return False

# Function to click the "Regenerate" button if found
def click_regenerate_button():
    scroll_to_bottom()
    try:
        regenerate_button = driver.find_element(By.CSS_SELECTOR, selectors["regenerate_button"])
        regenerate_button.click()
        print("Clicked 'Regenerate' button.")
        return True
    except Exception as e:
        print("No 'Regenerate' button found.")
        return False

# Function to redirect to the specific chat link and type the first 'Next' message
def redirect_to_chat_and_type_next(subject, unique_id):
    print(f"Redirecting to chat and typing '{subject} {unique_id}'...")
    driver.get(chatgpt_chat_link)
    # Wait for the textarea to be present
    textarea = WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selectors["textarea"]))
    )
    textarea.send_keys(f"{subject} {unique_id}")
    time.sleep(3)  # Add delay before clicking send button

    # Locate and click the send button
    send_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selectors["send_button"]))
    )
    send_button.click()
    print(f"'{subject} {unique_id}' message sent.")

# Function to send a message and wait for the response
def send_message_and_wait(subject, unique_id, part_id):
    print(f"Sending message: {subject} with ID {unique_id}.{part_id}")
    textarea = WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selectors["textarea"]))
    )
    textarea.send_keys(f"{subject} {unique_id}.{part_id}")
    time.sleep(3)  # Add delay before clicking send button

    # Locate and click the send button
    send_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selectors["send_button"]))
    )
    send_button.click()
    print(f"Message '{subject} {unique_id}.{part_id}' sent.")

# Function to wait for the response to be completely generated
def wait_for_response(unique_id, part_id, start_time, last_prompt, retry_count=0):
    print(f"Waiting for response to be completely generated with ID {unique_id}.{part_id}...")

    while True:
        try:
            elapsed_time = time.time() - start_time
            if elapsed_time > 900:  # 15 minutes in seconds
                if retry_count >= 3:
                    print("Waiting for too long. Taking a break for 1 hour and 10 minutes.")
                    time.sleep(4200)  # 1 hour and 10 minutes in seconds
                    return False
                print("Refreshing the page due to inactivity.")
                driver.refresh()
                time.sleep(5)
                if check_gpt4_limit():
                    send_message_and_wait(last_prompt["subject"], last_prompt["unique_id"], last_prompt["part_id"])
                    return wait_for_response(unique_id, part_id, time.time(), last_prompt, retry_count + 1)
                return wait_for_response(unique_id, part_id, time.time(), last_prompt, retry_count + 1)

            print("Checking for new div elements...")
            driver.execute_script("window.scrollTo(0, 0);")
            new_div_elements = driver.find_elements(By.CSS_SELECTOR, selectors["response_div"])
            print(f"Found {len(new_div_elements)} div elements.")
            total_id_count = 0
            for div_element in new_div_elements:
                # Debug: Print the text content of the div element
                div_text = div_element.text.strip()
                print(f"Div text: {div_text}")

                # Check if the div text contains the unique ID
                if f"{unique_id}.{part_id}" in div_text:
                    total_id_count += 1

            if total_id_count >= 1:  # Response should contain at least 1 occurrence of the unique ID
                print("Response is complete.")
                return True
            
            # Check for "Continue generating" or "Regenerate" buttons and click if found
            if not click_continue_generating():
                if click_regenerate_button():
                    print("Regenerate button clicked.")
                    time.sleep(5)
                    return wait_for_response(unique_id, part_id, time.time(), last_prompt, retry_count + 1)

            time.sleep(10)
        except Exception as e:
            print(f"Error while waiting for response: {e}")

        time.sleep(10)  # Check every 10 seconds

    print(f"Response received for ID {unique_id}.{part_id}")

# Function to copy the response
def copy_response(unique_id, part_id):
    print(f"Copying the response for ID {unique_id}.{part_id}...")
    # Locate the latest 'div' element and copy its content
    response_element = driver.find_elements(By.CSS_SELECTOR, selectors["response_div"])[-1]
    response_text = response_element.text
    response_text = response_text.replace(f"{unique_id}.{part_id}", '').strip()  # Remove the unique ID and part ID
    pyperclip.copy(response_text)
    print(f"Response copied: {response_text[:100]}...")  # Print first 100 characters for verification

# Function to clean and normalize the subject for file naming
def clean_subject(subject):
    return subject.split(':')[0].strip().replace('"', '').replace("'", '').replace(',', '')

# Function to save the response to a file
def save_response(subject, part_id, append=False):
    print(f"Saving the response for subject {subject}, part {part_id}...")
    response_text = pyperclip.paste()
    print(f"Copied response: {response_text[:100]}...")  # Print first 100 characters for verification

    # Clean the subject for the file name
    clean_subject_name = clean_subject(subject)
    
    # Define the file paths
    json_file_path = os.path.join(json_output_path, f"{clean_subject_name}.json")

    # Load existing data if appending
    if append and os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    try:
        # Append the new part
        data.extend(json.loads(response_text))

        # Save the response as a JSON file
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Response saved as {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"Error occurred while saving response: {e}")

# Main loop to process each subject and its parts
def main():
    last_processed_subject = read_last_processed_subject()
    start_index = 0

    if last_processed_subject and last_processed_subject in subjects:
        start_index = subjects.index(last_processed_subject) + 1

    input("Press Enter after logging in manually and being redirected to the chat...")

    # Run the pyautogui sequence once at the beginning
    reset_chat_history_with_pyautogui()

    for index, subject in enumerate(subjects[start_index:], start=start_index):
        unique_id = generate_unique_id()
        last_prompt = {"subject": subject, "unique_id": unique_id, "part_id": 1}
        
        for part_id in range(1, 15):  # Divide into 14 parts
            start_time = time.time()
            last_prompt["part_id"] = part_id
            try:
                send_message_and_wait(subject, unique_id, part_id)
                if not wait_for_response(unique_id, part_id, start_time, last_prompt):
                    continue  # Retry the same part if wait_for_response returns False
                copy_response(unique_id, part_id)
                save_response(subject, part_id, append=(part_id > 1))
                print(f"Saved part {part_id} of {subject} with ID {unique_id}.{part_id}")
                if part_id == 14:
                    save_last_processed_subject(subject)
                    if (part_id % 3) == 0:
                        driver.refresh()
                        time.sleep(5)
                        reset_chat_history_with_pyautogui()
            except Exception as e:
                print(f"Error occurred: {e}")
                driver.refresh()
                time.sleep(5)
                if check_gpt4_limit():
                    send_message_and_wait(last_prompt["subject"], last_prompt["unique_id"], last_prompt["part_id"])
                if (part_id % 3) == 0:
                    reset_chat_history_with_pyautogui()
                break  # Exit the loop for the current subject and retry the same part

if __name__ == "__main__":
    main()
