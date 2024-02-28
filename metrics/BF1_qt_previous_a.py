import json
import argparse
import csv
from bert_score import score, BERTScorer
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

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
        csv_writer.writerow(['BF1(qt, a<t):'])  # Writing header

        for line in file:
            data = json.loads(line)
            dialogue = data['dialogue']  # Dialogue is a list of alternating questions and answers

            total_f1 = 0
            num_comparisons = 0
            concatenated_previous_answers = ""  # Initialize empty string for concatenated previous answers

            for i in range(0, len(dialogue)):  # Iterate over all dialogue components
                if i % 2 == 0:  # Current component is a question
                    # Skip F1 score computation for the first question
                    if i != 0 and concatenated_previous_answers: 
                        current_question = dialogue[i]
                        f1_score = compute_f1(current_question,concatenated_previous_answers,scorer1)
                        total_f1 += f1_score
                        num_comparisons += 1
                else:
                    # Current component is an answer, append it to concatenated_previous_answers
                    concatenated_previous_answers += " " + dialogue[i]

            # Calculate average F1 score for this conversation
            average_f1 = total_f1 / num_comparisons if num_comparisons > 0 else 0
            csv_writer.writerow([average_f1])  # Writing average F1 score of each conversation





def main():
    parser = argparse.ArgumentParser(description="Process a JSONL file for QA scoring.")
    parser.add_argument("--file_path", type=str, help="Path to the JSONL file")
    parser.add_argument("--output_path", type=str, help="Path to the output CSV file")
    parser.add_argument("--device", type=str, default="cpu", choices=["cpu", "gpu"], help="Device to use (cpu or gpu)")

    args = parser.parse_args()

    process_jsonl(args.file_path, args.output_path, args.device)

if __name__ == "__main__":
    main()