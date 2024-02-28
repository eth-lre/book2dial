import json
import argparse
import csv
from transformers import pipeline

qa_model = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')

def unanswerability(question,  answer,context):
    if not question or not answer or answer.upper() == 'CANNOTANSWER':
        return 1
    if not question.endswith('?'):
        return 1
    # Step 1: Context Alignment
    model_answer = qa_model(question=question, context=context)["answer"]
    if not model_answer  or model_answer.upper() == 'CANNOTANSWER' or model_answer.lower().replace(" ", "") == "novaluejudgment":
        return 1
    else:
        return 0



def process_jsonl(file_path, output_path, device):
    device = 0 if device == 'gpu' else -1  # 0 for GPU (cuda), -1 for CPU

    with open(file_path, 'r') as file, open(output_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['Answerable Score:'])  # Writing header

        for line in file:
            data = json.loads(line)
            context = data['context']
            dialogue = data['dialogue']

            line_score = 0
            num_pairs = 0

            for i in range(0, len(dialogue), 2):
                question = dialogue[i]
                answer = dialogue[i + 1]
                score = unanswerability(question, answer, context)
                line_score += score
                num_pairs += 1

            average_score = line_score / num_pairs if num_pairs > 0 else 0
            average_score = 1 - average_score  # one minus unanswerable == answerable
            csv_writer.writerow([average_score])  # Writing average score of each line

def main():
    parser = argparse.ArgumentParser(description="Process a JSONL file for QA scoring.")
    parser.add_argument("--file_path", type=str, help="Path to the JSONL file")
    parser.add_argument("--output_path", type=str, help="Path to the output CSV file")
    parser.add_argument("--device", type=str, default="cpu", choices=["cpu", "gpu"], help="Device to use (cpu or gpu)")

    args = parser.parse_args()

    process_jsonl(args.file_path, args.output_path, args.device)

if __name__ == "__main__":
    main()