import json
import argparse
import csv
from newsroom.analyze import Fragments

def coverage(context, history):

    fragments = Fragments(history, context)
    return fragments.coverage()

def process_jsonl(file_path, output_path, device):

    with open(file_path, 'r') as file, open(output_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['Coverage:'])  # Writing header

        for line in file:
            data = json.loads(line)
            context = data['context']
            dialogue = data['dialogue']
            dialogue_text = ' '.join(dialogue)
            average_score = coverage(context,dialogue_text)
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