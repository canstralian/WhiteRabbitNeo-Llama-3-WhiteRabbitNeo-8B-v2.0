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


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/canstralian/WhiteRabbitNeo-Llama-3-WhiteRabbitNeo-8B-v2.0.git
   cd WhiteRabbitNeo-Llama-3-WhiteRabbitNeo-8B-v2.0
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the app:
   ```bash
   streamlit run app.py
   ```

4. (Optional, Recommended) Ensure GPU acceleration:
   - Install CUDA Toolkit [instructions link].
   - Verify PyTorch GPU support:
     ```bash
     python -c "import torch; print(torch.cuda.is_available())"
     ```

- **Interactive Interface**: Real-time interaction with the Llama 3 model.
- **Quantized Inference**: Optimize performance using 4-bit weights via `bitsandbytes`.
- **Caching**: Efficient resource reloading for faster runtime.

### **How the Project Works**
Details for each layer of the architecture (UI/Inference/Model Loading). Example:

```
The **model loading layer** applies `@st.cache_resource` to minimize reloads and enhance memory usage. Depending on configuration, the weights can be quantized prior to inference.
```

## Contributing

Contributions are welcome! Follow these steps:

1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request.
