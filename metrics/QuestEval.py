import json
import argparse
import csv
from questeval.questeval_metric import QuestEval

def process_jsonl(file_path, output_path, device):
    if device == 'gpu':
        questeval = QuestEval(no_cuda=False)
    else:
        questeval = QuestEval(no_cuda=True)
    with open(file_path, 'r') as file, open(output_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['QuestEval:'])  # Writing header

        for line in file:
            data = json.loads(line)
            context = data['context']
            dialogue = data['dialogue']

            line_score = 0
            num_pairs = 0

            for i in range(0, len(dialogue), 2):
                question = dialogue[i]
                answer = dialogue[i + 1]
                score = questeval.corpus_questeval(hypothesis=[question], sources=[answer])
                line_score += score['corpus_score']
                num_pairs += 1

            average_score = line_score / num_pairs if num_pairs > 0 else 0
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