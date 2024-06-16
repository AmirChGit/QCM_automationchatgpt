Create these files sub folders : Json_Files, Subject_source, Excel_QCM
Put the subjects source excel inside Subject_source, and update path on aut_chatgpt.py

Launch a Command Prompt and start a new chrome sessions with this command after updating paths :
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\path\to\your\chrome\profile"

Launch auto_chatgpt.py
_____________________________________________________________________________
ChatGPT Automation QCM Generation Prompt : Prompt JsonQCM_Project:

I need to generate 10 questions for each subject from a given list. The questions should be in three types: Multiple Choice, Fill in the Blanks, and True/False (make sur distribute the questions types evenly through the 10 questions). Each question be unique and valid and coherent with the subject, answer candidates (for multiple choice), the correct answer, and a brief analysis.  refer to the provided file security_studies.json for the required structure example. make sur to absolutely respect this structure, here's an example for the first question (the word preceded by the sign $ indicate an example of the value that you should replace it with) make sur to always include all the data even if blank, increment the 1 from 1 to 10,trimm the subject title, write the same question with in the field text and question, always write "English" in the question field, and leave ori , info and url blank with only "".
{
        "id": $unique_id,
        "title": $trimmed_subject example : "security_studies",
        "text": $question example : "True or False: Asymmetric warfare involves conflicts between parties of unequal strength, where the weaker party uses unconventional tactics.",
        "language": "English",
        "ori": leave only "",
	    "info":leave only "", 
        "url": leave only "",
        "subject": $subject example : "security_studies: ['politics']",
        "question_type": $question_type example : "judgment",
        "question": $same_question example "True or False: Asymmetric warfare involves conflicts between parties of unequal strength, where the weaker party uses unconventional tactics.",
        "answer": $answser example :"True",
        "analysis": $analysis example :"Asymmetric warfare involves conflicts between parties of unequal strength, where the weaker party uses unconventional tactics."
    },
and this is an example of a 10 questions format : 
[
    {
        "id": 1,
        "title": "security_studies",
        "text": "Which of the following is a key concept in security studies?",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "choice",
        "question": "Which of the following is a key concept in security studies?",
        "answer_candidates": [
            {"option": "A", "content": "Balance of Power"},
            {"option": "B", "content": "Economic Growth"},
            {"option": "C", "content": "Cultural Exchange"},
            {"option": "D", "content": "Technological Innovation"}
        ],

        "answer": "A",
        
        "analysis": "Balance of Power is a key concept in security studies."
    },
    {
        "id": 2,
        "title": "security_studies",
        "text": "The strategy aimed at preventing an adversary from taking an unwanted action through the threat of retaliation is known as ____.",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "fill_in_the_blank",
        "question": "The strategy aimed at preventing an adversary from taking an unwanted action through the threat of retaliation is known as ____.",
        "answer": "deterrence",
        "analysis": "The strategy aimed at preventing an adversary from taking an unwanted action through the threat of retaliation is known as deterrence."
    },
    {
        "id": 3,
        "title": "security_studies",
        "text": "True or False: The concept of human security includes both freedom from fear and freedom from want.",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "judgment",
        "question": "True or False: The concept of human security includes both freedom from fear and freedom from want.",
        "answer": "True",
        "analysis": "Human security includes both freedom from fear and freedom from want, emphasizing the protection of individuals."
    },
    {
        "id": 4,
        "title": "security_studies",
        "text": "Which international organization is primarily responsible for maintaining international peace and security?",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "choice",
        "question": "Which international organization is primarily responsible for maintaining international peace and security?",
        "answer_candidates": [
            {"option": "A", "content": "World Bank"},
            {"option": "B", "content": "United Nations"},
            {"option": "C", "content": "International Monetary Fund"},
            {"option": "D", "content": "World Trade Organization"}
        ],
        "answer": "B",
        "analysis": "The United Nations is primarily responsible for maintaining international peace and security."
    },
    {
        "id": 5,
        "title": "security_studies",
        "text": "What is the primary focus of cybersecurity?",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "choice",
        "question": "What is the primary focus of cybersecurity?",
        "answer_candidates": [
            {"option": "A", "content": "Economic Development"},
            {"option": "B", "content": "Protecting Digital Information"},
            {"option": "C", "content": "Environmental Protection"},
            {"option": "D", "content": "Promoting Cultural Heritage"}
        ],
        "answer": "B",
        "analysis": "The primary focus of cybersecurity is protecting digital information."
    },
    {
        "id": 6,
        "title": "security_studies",
        "text": "True or False: The theory of collective security involves states agreeing to respond collectively to threats and breaches of peace.",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "judgment",
        "question": "True or False: The theory of collective security involves states agreeing to respond collectively to threats and breaches of peace.",
        "answer": "True",
        "analysis": "The theory of collective security involves states agreeing to respond collectively to threats and breaches of peace."
    },
    {
        "id": 7,
        "title": "security_studies",
        "text": "The policy of increasing a nation's military capability to deter potential adversaries is known as ____.",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "fill_in_the_blank",
        "question": "The policy of increasing a nation's military capability to deter potential adversaries is known as ____.",
        "answer": "arms buildup",
        "analysis": "The policy of increasing a nation's military capability to deter potential adversaries is known as arms buildup."
    },
    {
        "id": 8,
        "title": "security_studies",
        "text": "Which document outlines the fundamental principles and guidelines for international humanitarian law?",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "choice",
        "question": "Which document outlines the fundamental principles and guidelines for international humanitarian law?",
        "answer_candidates": [
            {"option": "A", "content": "Universal Declaration of Human Rights"},
            {"option": "B", "content": "Geneva Conventions"},
            {"option": "C", "content": "Kyoto Protocol"},
            {"option": "D", "content": "Paris Agreement"}
        ],
        "answer": "B",
        "analysis": "The Geneva Conventions outline the fundamental principles and guidelines for international humanitarian law."
    },
    {
        "id": 9,
        "title": "security_studies",
        "text": "True or False: Asymmetric warfare involves conflicts between parties of unequal strength, where the weaker party uses unconventional tactics.",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "judgment",
        "question": "True or False: Asymmetric warfare involves conflicts between parties of unequal strength, where the weaker party uses unconventional tactics.",
        "answer": "True",
        "analysis": "Asymmetric warfare involves conflicts between parties of unequal strength, where the weaker party uses unconventional tactics."
    },
    {
        "id": 10,
        "title": "security_studies",
        "text": "The concept of ____ security emphasizes the protection of a state's sovereignty and territorial integrity.",
        "language": "English",
        "ori": "",
	    "info":"", 
        "url": "",
        "subject": "security_studies: ['politics']",
        "question_type": "fill_in_the_blank",
        "question": "The concept of ____ security emphasizes the protection of a state's sovereignty and territorial integrity.",
        "answer": "national",
        "analysis": "The concept of national security emphasizes the protection of a state's sovereignty and territorial integrity."
    }
]


The prompt format will always be like this : Next : $subject, $promptID
$promptIT is a unique id for this specific prompt. example : Next : anatomy": ["health"] 254896

Generate a response structured strictly and always only as follows : write only the text for each requested subject and at the end only write the $promptID given in the prompt and nothing else, write everything in a single bloc of plain text, await until you are given the instruction 'Next : '  followed by the requested subjet + a new promptID.
Do not write anything else i want the response to be only the requested information.