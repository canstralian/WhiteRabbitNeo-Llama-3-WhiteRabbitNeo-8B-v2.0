import os
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

MODEL_ID = os.getenv("MODEL_ID", "your-org/your-llama3-8b-model")

@st.cache_resource
def load_llm():
    # If running on GPU, 4-bit is usually the best fit for a single-GPU Space.
    use_4bit = torch.cuda.is_available()

    quant_config = None
    if use_4bit:
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,  # or torch.float16
        )

    tok = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        quantization_config=quant_config,
    )

    model.eval()
    return tok, model

def generate(tok, model, prompt, max_new_tokens, temperature):
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        out = model.generate(
            **inputs,
            do_sample=temperature > 0,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            pad_token_id=tok.eos_token_id,
        )
    return tok.decode(out[0], skip_special_tokens=True)

st.title("WhiteRabbitNeo Llama 3 8B")

tok, model = load_llm()

prompt = st.text_area("Prompt", height=150)
temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_new_tokens = st.number_input("Max new tokens", 16, 2048, 256)

if st.button("Run"):
    if not prompt.strip():
        st.warning("Enter a prompt.")
    else:
        st.write(generate(tok, model, prompt, int(max_new_tokens), float(temperature)))        st.text_area("", output, height=250)# Additional sections for visualizations, explanations, or other functionalities (optional)