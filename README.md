# Real-Time Question Detection and Answering from IP Camera Feed

This project captures a live video stream from an IP camera, detects text using OCR, identifies questions, and answers them using a local LLM (Mistral 7B in GGUF format) running on CPU.

## Features

- Real-time video capture from an IP camera
- Optical Character Recognition (OCR) with Tesseract
- Automatic detection of questions in the video
- Local LLM (no internet required) for answering questions
- Live visual feedback using OpenCV



## Requirements

- Python 3.8+
- OpenCV
- pytesseract
- llama-cpp-python
- A GGUF LLM model like `mistral-7b-instruct-v0.1.Q4_K_M.gguf`
- Tesseract OCR installed (with `tesseract` accessible in your PATH)

## Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

### Install Tesseract OCR (Linux example)

```bash
sudo apt update
sudo apt install tesseract-ocr
```

## Usage

1. Update the IP camera URL in `main.py`:
```python
ip_camera_url = 'http://your-camera-ip:port/video'
```

2. Set the correct path to your local `.gguf` model:
```python
llm = Llama(model_path="path/to/your-model.gguf")
```

3. Run the script:
```bash
python main.py
```

Press `q` to quit the video window.

## Model Download

You can download the Mistral model (GGUF format) from HuggingFace:
- https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

Place it in your project folder or adjust the path accordingly.

## Example Output

```
QUESTION: What is machine learning?
ANSWER : Machine learning is a subset of AI that enables systems to learn from data...
```

## License

MIT License. Feel free to use, modify, and share.

## Author

Onana Gregoire Legrand