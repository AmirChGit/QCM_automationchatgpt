from openai import OpenAI
import pandas as pd
import json
import os

# Set up your OpenAI API key
client = OpenAI(
    api_key="",
)

def generate_questions(subject, num_questions):
    prompt = f"Generate {num_questions} university-level mathematical quiz questions for the subject '{subject}'. Each quiz question should be followed by its type (solution, calculation, multiple choice, true/false, fill-in-the-blank), the correct answer, and a brief analysis. Give the answer in this order: Question, Subject, Question_Type, Answer, Analysis."
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=num_questions * 10,
    )
    print(completion)
    generated_text = completion.choices[0].message.content
    print("Generated Questions:\n", generated_text)  # Debugging print
    return generated_text

def create_question(id, subject, question_text, question_type, answer, analysis):
    return {
        "id": id,
        "title": "college_mathematics",
        "text": question_text,
        "language": "English",
        "ori": "website",
        "info": "",
        "url": "https://math-quiz.co.uk",
        "subject": f"college_mathematics: ['{subject}']",
        "question_type": question_type,
        "question": question_text,
        "answer_candidates": [],
        "answer": answer,
        "analysis": analysis
    }

def get_last_id_and_subject(json_file):
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, 'r') as f:
            data = json.load(f)
            if data:
                last_entry = max(data, key=lambda x: x['id'])
                return last_entry['id'], last_entry['subject'].split("['")[1].split("']")[0]
    return 0, None

# Read subjects from Excel file
excel_file = 'C:/Users/achachoui/Documents/repository/QCM_automationchatgpt/Subjects/Subjects.xlsx'  # Replace with your Excel file path
df = pd.read_excel(excel_file)

# Initialize question list and ID counter
questions = []
question_id, last_subject_processed = get_last_id_and_subject('Maths_College.json')
question_id += 1

def main():
    global questions, question_id  # Ensure these are treated as global variables
    global last_subject_processed

    for subject in df['Subjects']:
        if last_subject_processed and subject != last_subject_processed:
            continue  # Skip subjects until we reach the last processed one
        last_subject_processed = None  # Reset after reaching the last processed subject

        questions_generated = 0
        while questions_generated < 500:  # Generate at least 500 questions per subject
            remaining_questions = 500 - questions_generated
            current_batch_size = min(10, remaining_questions)

            # Get the questions from OpenAI
            generated_questions_batch = generate_questions(subject, current_batch_size)

            if not generated_questions_batch:
                print(f"No questions generated for subject: {subject}")
                continue

            # Split the batch into individual questions
            generated_questions = generated_questions_batch.split('\n\n')

            for generated_question in generated_questions:
                try:
                    parts = generated_question.split('\n')
                    question_text = parts[0].replace("Question:", "").strip()
                    question_type = parts[2].replace("Question_Type:", "").strip()
                    answer = parts[3].replace("Answer:", "").strip()
                    analysis = parts[4].replace("Analysis:", "").strip()
                except IndexError:
                    print(f"Improperly formatted question: {generated_question}. Attempting to parse...")
                    # Attempt to recover as much information as possible
                    question_text = question_text if 'question_text' in locals() else "Incomplete question"
                    question_type = question_type if 'question_type' in locals() else "Unknown"
                    answer = answer if 'answer' in locals() else "Unknown"
                    analysis = analysis if 'analysis' in locals() else "No analysis available"

                # Create the question structure
                question = create_question(question_id, subject, question_text, question_type, answer, analysis)

                # Append the question to the list
                questions.append(question)

                # Increment the ID counter
                question_id += 1

                # Increment the questions generated counter
                questions_generated += 1

            # Append to JSON file after generating each set of questions
            with open('Maths_College.json', 'r+') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
                existing_data.extend(questions)
                f.seek(0)
                json.dump(existing_data, f, indent=4)
                questions = []  # Clear the list after writing

            # Save progress
            last_subject_processed = subject
            save_checkpoint(subject, question_id)

def save_checkpoint(subject, question_id):
    with open('checkpoint.json', 'w') as f:
        json.dump({'subject': subject, 'question_id': question_id}, f)

# Run the main function
main()
