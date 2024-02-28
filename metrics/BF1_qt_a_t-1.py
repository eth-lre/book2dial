import json
import argparse
import csv
from bert_score import score, BERTScorer

def init_bert_scorer():
    """
    Initialize the BERTScorer with the DeBERTa model.
    """
    return BERTScorer(lang="en", model_type="microsoft/deberta-large-mnli")


scorer1 = init_bert_scorer()


def compute_f1(a_pred,a_gold , scorer):
    """
    Compute the BERTScore F1 between two sequences using the given BERTScorer.
    """
    bert_scores = scorer.score([a_pred], [a_gold],verbose=False)
    P, R, f1 = (tensor.mean().item() for tensor in bert_scores)
    return f1
def process_jsonl(file_path, output_path, device):
    device = 0 if device == 'gpu' else -1  # 0 for GPU (cuda), -1 for CPU

    with open(file_path, 'r') as file, open(output_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['BF1(qt,a_(t-1)) score:'])  # Writing header

        for line in file:
            data = json.loads(line)
            context = data['context']
            dialogue = data['dialogue']

            line_score = 0
            num_pairs = 0

            for i in range(2, len(dialogue), 2):  # Start from the second question-answer pair
                question = dialogue[i]  # Current question
                previous_answer = dialogue[i - 1]  # Previous answer
                score = compute_f1(question, previous_answer, scorer1)  # Compute F1 between current question and previous answer
                line_score += score
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