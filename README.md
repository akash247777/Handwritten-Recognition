# Handwritten PDF to Text & Summary

This Streamlit application processes PDFs containing handwritten text, extracts the text using OCR technology, and generates an AI-powered summary of the content using Google's Gemini model.

## Features

- **Text Extraction:** Converts handwritten text in PDFs to machine-readable text using Tesseract OCR.
- **AI Summarization:** Summarizes extracted text using the Gemini-1.5-pro model from Google Generative AI.
- **User Interface:** Provides a web-based interface built with Streamlit for uploading PDFs, viewing extracted text, and downloading results.
- **Progress Tracking:** Displays a progress bar during text extraction for a better user experience.
- **Downloadable Outputs:** Allows users to download both the extracted text and the generated summary as `.txt` files.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- Tesseract OCR (ensure the executable path is correctly set in `main.py`)
- Poppler (ensure the path to `poppler/bin` is correctly set in `main.py`)

## Installation

### Clone the Repository
```bash
git clone https://github.com/your-username/handwritten-pdf-to-text-summary.git
cd handwritten-pdf-to-text-summary
```
### Create a Virtual Environment (optional but recommended)

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```
pip install -r requirements.txt
```
### Install Tesseract OCR

- Download and install Tesseract OCR from here.

- Update the `pytesseract.pytesseract.tesseract_cmd` path in main.py to point to your Tesseract executable (e.g.,` C:\Program Files\Tesseract-OCR\tesseract.exe)`.

### Install Poppler

- Download Poppler for Windows from here or install it via a package manager (`conda install poppler`).

- Update the `poppler_path` in `main.py `to point to your Poppler bin directory (e.g., `C:\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin`).

### Obtain a Google API Key

1. Create a project in the Google Cloud Console.

2. Enable the Generative AI API and generate an API key.

3. Use this key in the application sidebar when prompted.

#### Usage

### Run the Application

```
streamlit run main.py
```
### Access the Web Interface

- Open your browser and navigate to http://localhost:8501 (or the URL provided by Streamlit).

- Upload a PDF containing handwritten text.

- Enter your Google API key in the sidebar for summarization.

- Click "Process PDF" to extract text and generate a summary.

### View and Download Results

- The extracted text and summary are displayed in separate tabs.

- Use the download buttons to save the extracted text and summary as .txt files.


### Notes

- Ensure Tesseract and Poppler paths are correctly configured in main.py to avoid runtime errors.

- The application handles large PDFs by splitting text into chunks for summarization, ensuring compatibility with the Gemini model's token limits.

- The Google API key is required only for summarization; text extraction works without it.

- The application uses temporary files for PDF processing, which are automatically deleted after use.

### Troubleshooting

- Tesseract Not Found: Verify the Tesseract executable path in main.py and ensure Tesseract is installed.

- Poppler Not Found: Check the Poppler path in main.py and ensure Poppler is installed.

- API Key Errors: Ensure the Google API key is valid and the Generative AI API is enabled in your Google Cloud project.

- Memory Issues: For very large PDFs, consider increasing system memory or reducing the PDF size.


