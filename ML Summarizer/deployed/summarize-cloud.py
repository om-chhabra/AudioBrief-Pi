import json
from transformers import BartForConditionalGeneration, BartTokenizer
import nltk
import torch
from nltk.tokenize import sent_tokenize
from functions_framework import http

def check_and_download_punkt():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

# Check and download punkt if not present
check_and_download_punkt()

def clean_text(text):
    text = text.replace('\n', ' ')  # Replace newlines with spaces
    return text

def save_output_file(summary, confidence_score=0, reduction_percentage=0):
    result = {
        "Summarized Text": summary,
        "Average Confidence Score": f"{confidence_score:.2f}%",
        "Reduction in word count": f"{reduction_percentage:.2f}%"
    }
    return json.dumps(result)

@http
def summarize_http(request):
    request_json = request.get_json(silent=True)
    input_text = request_json.get('input_text')
    min_length, max_length = request_json.get('min_length'), request_json.get('max_length')

    cleaned_text = clean_text(input_text)

    # Load the model and tokenizer
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    # Tokenize and generate summary
    inputs = tokenizer(cleaned_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_output = model.generate(inputs["input_ids"], num_beams=4, min_length=min_length, max_length=max_length, early_stopping=True, return_dict_in_generate=True, output_scores=True)

    # Extract generated token ids and scores
    generated_token_ids = summary_output.sequences
    scores = summary_output.scores

    # Calculating average logit scores for the summary
    if scores:
        avg_scores = [torch.softmax(score, dim=-1).max(-1).values.mean().item() for score in scores]
        avg_confidence_score = sum(avg_scores) / len(avg_scores) * 100
    else:
        avg_confidence_score = 0

    summarized_text = tokenizer.decode(generated_token_ids[0], skip_special_tokens=True)

    # Convert summary to bullet points and calculate metrics
    sentences = sent_tokenize(summarized_text)
    bullet_points = "\n".join([f"- {sentence}" for sentence in sentences])
    original_word_count = len(cleaned_text.split())
    summarized_word_count = len(summarized_text.split())
    reduction_percentage = (original_word_count - summarized_word_count) / original_word_count * 100

    # Save the summary to a file
    result = save_output_file(bullet_points, confidence_score=avg_confidence_score, reduction_percentage=reduction_percentage)
    # Empty GPU memory
    torch.cuda.empty_cache()

    # Delete unnecessary objects and variables
    del cleaned_text
    del inputs
    del summary_output
    del generated_token_ids
    del scores
    del avg_scores
    del summarized_text
    del sentences

    # Delete the model and tokenizer to free up memory
    del model
    del tokenizer
    
    return result
