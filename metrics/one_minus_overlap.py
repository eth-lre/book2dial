import json
import argparse
import csv

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

def overlap(a_gold, a_pred):
    """
    Compute the word-level overlap between two sequences, modified to handle different lengths.
    """
    lemmatizer = WordNetLemmatizer()

    # Lemmatize and split the sequences into sets of words
    gold_toks = set([lemmatizer.lemmatize(word) for word in a_gold.split()])
    pred_toks = set([lemmatizer.lemmatize(word) for word in a_pred.split()])

    # Find the common tokens between the two sets
    common_toks = gold_toks.intersection(pred_toks)

    # The overlap is the number of common tokens divided by the number of tokens in the longer sequence
    max_len = max(len(gold_toks), len(pred_toks))
    if max_len == 0:
        return 0  # Avoid division by zero

    overlap = len(common_toks) / max_len
    return overlap
def process_jsonl(file_path, output_path, device):
    device = 0 if device == 'gpu' else -1  # 0 for GPU (cuda), -1 for CPU

    with open(file_path, 'r') as file, open(output_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['1-overlap(at,a<t) score:'])  # Writing header

        for line in file:
            data = json.loads(line)
            dialogue = data['dialogue']  # Dialogue is a list of alternating questions and answers

            total_overlap = 0
            num_comparisons = 0
            concatenated_previous_answers = ""  # Initialize empty string for concatenated previous answers

            # Iterate through each answer (at odd indices) and compare it with the concatenation of all previous answers
            for i in range(1, len(dialogue), 2):  # Iterate over answers only, starting from index 1
                current_answer = dialogue[i]

                if i > 1:  # If there are previous answers
                    if current_answer == "CANNOTANSWER" or current_answer.strip() == "":
                        score = 1
                    else:
                        score = overlap(current_answer,concatenated_previous_answers)
                    total_overlap += score
                    num_comparisons += 1

                concatenated_previous_answers += " " + current_answer  # Update the concatenated string

            # Calculate average overlap for this conversation
            average_overlap = total_overlap / num_comparisons if num_comparisons > 0 else 0
            result = 1 - average_overlap
            csv_writer.writerow([result])  # Writing average overlap of each conversation








def main():
    parser = argparse.ArgumentParser(description="Process a JSONL file for QA scoring.")
    parser.add_argument("--file_path", type=str, help="Path to the JSONL file")
    parser.add_argument("--output_path", type=str, help="Path to the output CSV file")
    parser.add_argument("--device", type=str, default="cpu", choices=["cpu", "gpu"], help="Device to use (cpu or gpu)")

    args = parser.parse_args()

    process_jsonl(args.file_path, args.output_path, args.device)

if __name__ == "__main__":
    main()