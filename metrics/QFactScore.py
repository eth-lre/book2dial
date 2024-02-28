import json
import argparse
import csv
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity

embed_model = SentenceTransformer('msmarco-distilbert-cos-v5') 
qa_model = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')

def compute_similarity(question, answer):
    embeddings = embed_model.encode([question, answer])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return similarity


def QFactScore_new(question, answer, context):
    if not question or not answer or answer.upper() == 'CANNOTANSWER':
        return 0
    if not question.endswith('?'):
        return 0

    model_answer = qa_model(question=question, context=context)["answer"]
    context_alignment = compute_similarity(answer.lower(), model_answer.lower() )

    # Step 2: Answer Relevance
    answer_relevance = compute_similarity(question.lower(), answer.lower())
    alpha = 1
    beta = 1
    # Final CAA score
    return alpha*context_alignment + beta*answer_relevance

def process_jsonl(file_path, output_path, device):
    device = 0 if device == 'gpu' else -1  # 0 for GPU (cuda), -1 for CPU

    with open(file_path, 'r') as file, open(output_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['QFactScore:'])  # Writing header

        for line in file:
            data = json.loads(line)
            context = data['context']
            dialogue = data['dialogue']

            line_score = 0
            num_pairs = 0

            for i in range(0, len(dialogue), 2):
                question = dialogue[i]
                answer = dialogue[i + 1]
                score = QFactScore_new(question, answer, context)
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