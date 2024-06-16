import os
import json
import pandas as pd
import time

def format_content(entry):
    subject_trimmed = entry["subject"].split(":")[0]
    answer_candidates = entry.get("answer_candidates", "null")
    
    # For fill-in-the-blank questions, set the answer in answer_candidates
    if entry["question_type"] == "fill_in_the_blank":
        answer_candidates = entry["answer"]

    formatted_content = (
        f'Subject:"{subject_trimmed}"\n'
        f'Question type:{entry["question_type"]}\n'
        f'Question:{entry["question"]}\n'
        f'Answer candidate:{json.dumps(answer_candidates)}\n'
        f'Answer:{entry["answer"]}\n'
        f'Analysis:{entry["analysis"]}'
    )
    return formatted_content

def create_new_excel_from_json(json_directory, new_excel_path, log_path, retries=3):
    all_data = []

    # Load the log file if it exists
    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            log_content = log_file.read().strip()
            if ',' in log_content:
                last_processed_file, last_processed_question = log_content.split(',')
                print(f"Last processed file: {last_processed_file}, Last processed question ID: {last_processed_question}")
            else:
                last_processed_file, last_processed_question = None, None
                print("Log file is not in the expected format. Starting from the beginning.")
    else:
        last_processed_file, last_processed_question = None, None
        print("No log file found. Starting from the beginning.")

    # Iterate over each JSON file in the specified directory
    json_files = sorted(os.listdir(json_directory))
    for filename in json_files:
        if filename.endswith(".json"):
            if last_processed_file and filename < last_processed_file:
                print(f"Skipping already processed file: {filename}")
                continue  # Skip files that have already been processed
            file_path = os.path.join(json_directory, filename)
            print(f"Processing file: {file_path}")

            # Read the JSON file
            with open(file_path, 'r') as file:
                json_data = json.load(file)

                for i, entry in enumerate(json_data):
                    question_id = entry.get('id', '')
                    if last_processed_file == filename and last_processed_question and str(question_id) <= last_processed_question:
                        print(f"Skipping already processed question ID: {question_id} in file: {filename}")
                        continue  # Skip questions that have already been processed

                    retries_left = retries
                    while retries_left > 0:
                        try:
                            subject_trimmed = entry["subject"].split(":")[0]
                            content = format_content(entry)  # Format JSON object to string
                            all_data.append({'Subject': subject_trimmed, 'Content': content})

                            # Log the last processed file and question
                            with open(log_path, 'w') as log_file:
                                log_file.write(f"{filename},{question_id}")
                            print(f"Processed question ID: {question_id} in file: {filename}")
                            break
                        except Exception as e:
                            print(f"Error processing {filename}, question {question_id}: {e}")
                            retries_left -= 1
                            time.sleep(1)  # Wait before retrying
                    else:
                        print(f"Failed to process {filename}, question {question_id} after {retries} retries")
                        return

    # Create a new dataframe with all collected data
    df = pd.DataFrame(all_data)

    # Save the new dataframe to a new Excel file
    try:
        with pd.ExcelWriter(new_excel_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        print("Data successfully written to the new Excel file.")
    except Exception as e:
        print(f"Error writing to the new Excel file: {e}")

# Usage
json_directory = 'D:/work/freelance/Json_QCMs/Json_Files'
new_excel_path = 'D:/work/freelance/Json_QCMs/Excel_qcm/new_export.xlsx'
log_path = 'D:/work/freelance/Json_QCMs/log.txt'
create_new_excel_from_json(json_directory, new_excel_path, log_path)
