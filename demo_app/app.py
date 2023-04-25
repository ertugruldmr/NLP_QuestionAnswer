import os
import pickle
import numpy as np
import gradio as gr
import transformers
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering, pipeline


# File Paths
model_path = 'fine_tuned_qa' 
tokenizer_path = "tokenizer"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# Load the fine-tuned BERT model
seq2seq_model = TFAutoModelForQuestionAnswering.from_pretrained(model_path)

# Creating the pipeline
qa_params = {
    "model":seq2seq_model,
    "tokenizer":tokenizer,
    "framework":"tf"
}

qa_pipeline = pipeline("question-answering", **qa_params)


# loading the example cases to test
with open("examples.pkl","rb") as f: examples = pickle.load(f)

# Define a function to make predictions with the model
def answear_question(text,question):

    # defining the params
    prms = {
        "min_length":5,
        "max_length":128
    }
    return qa_pipeline(text, question,**prms)["answer"]

# GUI Component
with gr.Blocks() as demo:
    context = gr.Textbox(label="context")
    question = gr.Textbox(label="question")
    act_ans = gr.Textbox(label="actual answer")
    gen_ans = gr.Button("Generate Answer")
    pred_ans = gr.Textbox(label="predicted answer")
    
    gen_ans.click(fn=answear_question, inputs=[context, question], outputs=pred_ans)

    gr.Examples(examples, inputs=[context, question,act_ans])


# Launching the demo
if __name__ == "__main__":
    demo.launch()
