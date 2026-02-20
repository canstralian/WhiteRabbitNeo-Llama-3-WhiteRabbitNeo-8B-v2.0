# WhiteRabbitNeo Llama 3 8B — Streamlit Interface

An interactive Streamlit application for running the WhiteRabbitNeo Llama 3 8B model directly inside a Hugging Face Space.

This project loads the model locally within the Space container and performs inference on GPU using PyTorch + Transformers.

---

## Overview

This application:

- Loads an 8B Llama 3 model at runtime
- Supports 4-bit quantized inference (optional)
- Uses Streamlit for the user interface
- Runs fully inside a Hugging Face GPU Space
- Caches the model to avoid reload on every interaction

The architecture separates:
- UI layer (Streamlit)
- Model loading layer (cached resource)
- Inference layer (generate function)

---

## Hardware Requirements

Recommended:

- GPU Space (T4 16GB minimum)
- 24GB VRAM preferred for FP16 inference
- Persistent storage enabled (recommended)

CPU Spaces are not suitable for interactive 8B inference.

---

## Model Loading Strategy

The model is loaded once using:

```python
@st.cache_resource

This ensures:
	•	No reload on UI interaction
	•	Faster response after first initialization
	•	Stable memory behavior during session lifecycle

Optional 4-bit quantization is enabled via bitsandbytes.

⸻

Deployment Instructions
	1.	Create a new Hugging Face Space
	2.	Select:
	•	SDK: Streamlit
	•	Hardware: GPU (T4 or higher)
	3.	Upload:
	•	app.py
	•	requirements.txt
	•	README.md
	4.	(Optional but recommended) Enable persistent storage
	5.	Set environment variable: