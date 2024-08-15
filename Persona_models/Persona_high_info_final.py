# final version

import os
import json
import time
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

def generate_prompt1(chapter_title, section_title, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation):
    prompt = ( "Task: You are a student preparing to ask questions about a textbook subsection to a teacher. "
    "Your goal is to uncover the key information from this subsection. Based on the teacher's responses, "
    "you'll further inquire to get a comprehensive understanding. Make sure to ask specific questions about "
    "the subsection's content and avoid repeating queries from prior discussions.\n\n"
    "Information Provided:\n"
    f"1. **Section Title:** {chapter_title}\n"
    f"2. **Subsection Title:** {section_title}\n"
    f"3. **Section Summary:** {chapter_summary}\n"
    f"4. **Bold Terms in Section:** {bold_terms}\n"
    f"5. **Learning Objectives:** {learning_objectives}\n"
    f"6. **Concepts in Section:** {concepts}\n"
    f"7. **Section Introduction:** {introduction}\n\n"
    "Previous Conversation:\n"
    f"{previous_conversation}\n\n"
    "*Note:* Frame your questions considering the information above and ensure they're relevant to the content. Do not ask question about information you already have. Only ask one question at a time.\n\n"
    "Expected Output: Please phrase your question as a string.")
    
    return prompt
def generate_prompt2(chapter_title, section_title,context, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation,question):
    prompt = ("Task: You are a teacher preparing to answer a student's question about a subsection of a textbook. "
    f"The student's question is: {question}. Provide a concise, specific response, ensuring it's not a summary and "
    f"distinct from any previous answers you've given.\n\n"
    f"Information Provided:\n"
    f"1. **Section Title:** {chapter_title}\n"
    f"2. **Subsection Title:** {section_title}\n"
    f"3. **Subsection Content:** {context}\n"
    f"4. **Section Summary:** {chapter_summary}\n"
    f"5. **Bold Terms in Section:** {bold_terms}\n"
    f"6. **Learning Objectives:** {learning_objectives}\n"
    f"7. **Concepts in Section:** {concepts}\n"
    f"8. **Section Introduction:** {introduction}\n\n"
    f"Previous Conversation:\n"
    f"{previous_conversation}\n\n"
    f"*Note:* When crafting your response, consider all the information above. Be sure your answer directly "
    f"addresses the student's question and is not a repetition of prior information.\n\n"
    f"Expected Output: Please phrase your answer as a string.")
    
    return prompt
def generate_response0(prompt, model):
    while True:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
             )
            return completion
        except:
            print("Error occurred while generating response. Retrying in 2 seconds...")
            time.sleep(2)

def generate_question(chapter_title, section_title, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation, model):
    prompt = generate_prompt1(chapter_title, section_title, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation)
    completion = generate_response0(prompt, model)
    question = completion.choices[0].message.content
    # escaped_content = question.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
    return question
def generate_answer(question, context, chapter_title, section_title, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation, model):
    if not question:
        print('Empty question was given as input.')
        return None
    prompt = generate_prompt2(chapter_title, section_title, context, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation,question)
    completion = generate_response0(prompt, model)
    answer = completion.choices[0].message.content
    # escaped_content = answer_data.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
    return answer

# Can use different models to do this task, for example: gpt-4o
model_name = "gpt-3.5-turbo"

def make_json_friendly(s):
    # Escape backslashes
    s = s.replace("\\", "\\\\")
    # Escape double quotes
    s = s.replace('"', '\\"')
    return s

def generate_dialog_for_section(section, model_name, turns=12):
    chapter_title = section["title"]
    paragraphs = section["paragraphs"]
    context = paragraphs[0]["context"]
    bold_terms = ', '.join(term.strip() for term in section['bold_terms'])
    
    section_title = section["section_title"]
    chapter_summary = section['chapter_summary']
    learning_objectives = ', '.join(objective.strip() for objective in section['chapter_learning_objectives'])
    concepts = ', '.join(concept['name'].strip() for concept in section['chapter_concept'])
    introduction = section['chapter_introduction']
    previous_conversation = ""
    
    
    dialogs = []
    for _ in range(turns // 2):
        question = generate_question(chapter_title, section_title, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation, model_name)
        # print('question:',question)
        
        answer = generate_answer(question, context, chapter_title, section_title, chapter_summary, bold_terms, learning_objectives, concepts, introduction, previous_conversation, model_name)
        # print('answer:',answer)

        
        dialogs.append({
            "question": question,
            "answer": answer
        })
        previous_conversation += f"\nStudent: {question}\nTeacher: {answer}"
    
    return dialogs

def append_to_jsonl(dialog, filename):
    with open(filename, "a") as outfile:
        outfile.write(json.dumps(dialog))
        outfile.write("\n")

def check_current_progress(filename):
    """
    Check the current progress by counting how many subsections have been completed.
    Return the index of the next subsection to process.
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            completed_sections = len(lines)
        return completed_sections
    except FileNotFoundError:
        return 0

def generate_and_save_dialogs(data, model_name, filename, turns=12):
    # Check current progress
    start_section = check_current_progress(filename)
    print('start_section',start_section)
    for idx, section in enumerate(data["data"][start_section:], start=start_section):
        print(f"Generating dialogs for subsection {idx + 1}/{len(data['data'])}")
        dialogs = generate_dialog_for_section(section, model_name, turns)
        dialog_data = {
            "title": section["title"],
            "context":section["paragraphs"][0]['context'],
            "dialogs": dialogs
            
        }
        append_to_jsonl(dialog_data, filename)

if __name__ == "__main__":
    # Load the data
    with open("./example_textbook_data/example.json", "r") as file:
        data = json.load(file)

    # Generate and save the dialogs
    output_filename = "test_science_high_info.jsonl"
    generate_and_save_dialogs(data, model_name, output_filename)
    print(f"Generation finished, dialogs saved to {output_filename}")
