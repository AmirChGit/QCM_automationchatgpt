import os
import time
import json
import pyperclip
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the Excel file containing the subjects
excel_path = "D:/work/freelance/Json_QCMs/Subject_source/Subjects.xlsx"
last_processed_subject_file = "D:/work/freelance/Json_QCMs/last_Maths_subject.txt"
chatgpt_chat_link = "https://chatgpt.com/c/d082061f-e257-4a31-9e7d-5b55e02cf914"
json_output_path = "D:/work/freelance/Json_QCMs/College_Maths_Milestone_1"

# Read subjects from the first column of the Excel file
df = pd.read_excel(excel_path)
subjects = df.iloc[:, 0].dropna().tolist()

# Define element selectors
selectors = {
    "textarea": 'div.flex.min-w-0.flex-1.flex-col textarea.m-0.resize-none.border-0.bg-transparent.px-0.text-token-text-primary.focus\\:ring-0.focus-visible\\:ring-0',
    "send_button": 'div.flex.items-end.gap-1\\.5.md\\:gap-2 > button:nth-child(3)',
    "response_div": 'div.markdown.prose.w-full.break-words.dark\\:prose-invert.dark',
    "first_button": '.flex.h-9.w-9.items-center.justify-center.rounded-full.text-token-text-secondary.transition.hover\\:bg-token-main-surface-tertiary',
    "second_button": '.btn.relative.btn-primary',
    "second_button_child": '.flex.items-center.justify-center',
    "continue_button": '.btn.relative.btn-secondary.whitespace-nowrap.border-0.md\\:border',
    "continue_button_child": 'div.flex.items-center.justify-center'
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

# Function to normalize text by removing spaces and newline characters
def normalize_text(text):
    return ''.join(text.split())

# Function to perform the additional actions before sending the next prompt
def perform_additional_actions():
    print("Performing additional actions before sending the next prompt...")
    try:
        # Click the first button with the specified class
        first_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selectors["first_button"]))
        )
        first_button.click()
        print("First button clicked.")

        # Find and click the second button with the specified class and child div
        buttons = driver.find_elements(By.CSS_SELECTOR, selectors["second_button"])
        for button in buttons:
            child_div = button.find_element(By.CSS_SELECTOR, selectors["second_button_child"])
            if child_div.text == "Send":
                button.click()
                print("Second button clicked.")
                break
        time.sleep(5)
    except Exception as e:
        print(f"Error performing additional actions: {e}")

# Function to click the "Continue generating" button if found
def click_continue_generating():
    try:
        continue_button = driver.find_element(By.CSS_SELECTOR, selectors["continue_button"])
        continue_button.click()
        print("Clicked 'Continue generating' button.")
    except Exception as e:
        print("No 'Continue generating' button found.")

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
def send_message_and_wait(subject, unique_id):
    perform_additional_actions()
    print(f"Sending message: {subject} with ID {unique_id}")
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
    print(f"Message '{subject} {unique_id}' sent.")

# Function to wait for the response to be completely generated
def wait_for_response(unique_id, start_time):
    print(f"Waiting for response to be completely generated with ID {unique_id}...")

    while True:
        try:
            elapsed_time = time.time() - start_time
            if elapsed_time > 5400:  # 1 hour and 30 minutes in seconds
                print("Waiting for too long. Taking a break for 1 hour and 10 minutes.")
                time.sleep(4200)  # 1 hour and 10 minutes in seconds
                return

            print("Checking for new div elements...")
            new_div_elements = driver.find_elements(By.CSS_SELECTOR, selectors["response_div"])
            print(f"Found {len(new_div_elements)} div elements.")
            total_id_count = 0
            for div_element in new_div_elements:
                # Debug: Print the text content of the div element
                print("Div text content: ", div_element.text)
                count_id = div_element.text.count(unique_id)
                total_id_count += count_id
                print(f"Found {count_id} occurrences of ID {unique_id} in a div element.")
            print(f"Total occurrences of ID {unique_id} across all div elements: {total_id_count}")
            if total_id_count >= 1:
                print(f"Detected unique ID {unique_id} in the response.")
                time.sleep(8)  # Wait for 8 seconds to ensure the response is fully generated
                return
            click_continue_generating()  # Check for "Continue generating" button and click it if found
            time.sleep(10)
        except Exception as e:
            print(f"Error while checking for new elements: {e}")
            time.sleep(1)

# Function to copy the response
def copy_response(unique_id):
    print(f"Copying the response for ID {unique_id}...")
    # Locate the latest 'div' element and copy its content
    response_element = driver.find_elements(By.CSS_SELECTOR, selectors["response_div"])[-1]
    response_text = response_element.text
    response_text = response_text.replace(unique_id, '').strip()  # Remove the unique ID from the response
    pyperclip.copy(response_text)
    print(f"Response copied: {response_text[:100]}...")  # Print first 100 characters for verification

# Function to clean and normalize the subject for file naming
def clean_subject(subject):
    return subject.split(':')[0].strip().replace('"', '').replace("'", '').replace(',', '')

# Function to save the response to a file
def save_response(subject):
    print(f"Saving the response for subject {subject}...")
    response_text = pyperclip.paste()
    print(f"Copied response: {response_text[:100]}...")  # Print first 100 characters for verification

    # Clean the subject for the file name
    clean_subject_name = clean_subject(subject)
    
    # Define the file paths
    txt_file_path = os.path.join(json_output_path, f"{clean_subject_name}.txt")
    json_file_path = os.path.join(json_output_path, f"{clean_subject_name}.json")

    # Save the response as a text file
    with open(txt_file_path, 'w') as file:
        file.write(response_text)
    print(f"Response saved as {txt_file_path}")

    # Rename the text file to a JSON file
    os.rename(txt_file_path, json_file_path)
    print(f"File renamed to {json_file_path}")

# Main loop to perform actions and handle errors
def main():
    last_processed_subject = read_last_processed_subject()
    start_index = 0

    if last_processed_subject and last_processed_subject in subjects:
        start_index = subjects.index(last_processed_subject) + 1
    else:
        last_processed_subject = subjects[0]

    input("Press Enter after logging in manually and being redirected to the chat...")

    for index, subject in enumerate(subjects[start_index:], start=start_index):
        unique_id = generate_unique_id()
        start_time = time.time()
        try:
            send_message_and_wait(subject, unique_id)
            wait_for_response(unique_id, start_time)
            copy_response(unique_id)
            save_response(subject)
            save_last_processed_subject(subject)
        except Exception as e:
            print(f"Error occurred: {e}")
            driver.refresh()
            unique_id = generate_unique_id()
            redirect_to_chat_and_type_next(subject, unique_id)

if __name__ == "__main__":
    main()

