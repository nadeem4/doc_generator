import argparse
import os
import sys
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def summarize_code(code_snippet, tokenizer, model):
    inputs = tokenizer.encode(code_snippet, return_tensors='pt', truncation=True, max_length=512)
    outputs = model.generate(
        inputs,
        max_length=150,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary.strip()

def generate_description(file_path, model_name='Salesforce/codet5-small'):
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Read the entire code file
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    # Summarize the code
    print("Summarizing the code...")
    module_summary = summarize_code(code, tokenizer, model)

    # Prepare markdown content
    md_content = f"# Module Summary\n\n{module_summary}\n"

    return md_content

def main():
    parser = argparse.ArgumentParser(description='Generate markdown description from Python file.')
    parser.add_argument('file_path', help='Path to the Python (.py) file.')
    parser.add_argument('--model-name', default='Salesforce/codet5-small', help='Name of the open-source LLM to use.')
    args = parser.parse_args()

    file_path = args.file_path
    model_name = args.model_name

    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)

    description = generate_description(file_path, model_name)

    md_file_path = os.path.splitext(file_path)[0] + '.md'
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(description)

    print(f"Markdown description generated and saved to {md_file_path}")

if __name__ == '__main__':
    main()
