import streamlit as st
import pytesseract
from PIL import Image
import pdf2image
import io
import tempfile
import os
import re

# Set the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Adjust this path to where you installed Tesseract

# Rest of your imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain_google_genai import ChatGoogleGenerativeAI

# Set page configuration
st.set_page_config(
    page_title="Handwritten PDF to Text & Summary",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("📝 Handwritten PDF to Digital Text & Summary")
st.markdown("""
This application processes PDFs containing handwritten text and:
1. Extracts the handwritten content using OCR technology
2. Converts it to clean, machine-readable text
3. Generates an AI-powered summary of the content
""")

# Create sidebar for API key
with st.sidebar:
    st.header("Configuration")
    google_api_key = st.text_input("Enter your Google API Key", type="password", 
                                   help="Required for generating summaries")
    
    # Set the Google API key
    if google_api_key:
        os.environ["GOOGLE_API_KEY"] = google_api_key
    
    st.markdown("---")
    st.markdown("""
    ### How it works
    
    1. Upload a PDF file containing handwritten text
    2. Our app converts each page to an image
    3. OCR technology extracts the text
    4. AI processes and summarizes the extracted content
    5. View both the extracted text and summary
    """)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app uses Tesseract OCR for text extraction and Google's Gemini model for summarization.")

# Initialize session state variables if they don't exist
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# Function to extract text from PDF using OCR
def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(pdf_file.getvalue())
        pdf_path = tmp_file.name
    
    # Specify the path to poppler
    poppler_path = r"C:\\Downloads\\Release-24.08.0-0\\poppler-24.08.0\\Library\\bin"  # Adjust this path to where you installed poppler
    
    # Convert PDF to images
    images = pdf2image.convert_from_path(pdf_path, poppler_path=poppler_path)
    os.unlink(pdf_path)  # Delete temporary file
    
    full_text = ""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, img in enumerate(images):
        status_text.text(f"Processing page {i+1}/{len(images)}...")
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img)
        full_text += f"\n\n--- Page {i+1} ---\n\n{text}"
        
        # Update progress
        progress_bar.progress((i + 1) / len(images))
    
    status_text.empty()
    progress_bar.empty()
    
    # Clean up the extracted text
    cleaned_text = clean_extracted_text(full_text)
    return cleaned_text

# Function to clean up the extracted text
def clean_extracted_text(text):
    # Remove excessive whitespace
    cleaned = re.sub(r'\s+', ' ', text)
    # Remove any non-alphanumeric characters that might be OCR artifacts
    cleaned = re.sub(r'[^\w\s.,;:!?()[\]{}"\'-]', '', cleaned)
    # Fix common OCR errors
    cleaned = cleaned.replace('|', 'I').replace('0', 'O')
    return cleaned

# Function to generate summary using Google's Gemini model
def generate_summary(text, google_api_key):
    if not text.strip():
        return "No text was extracted to summarize."
    
    if not google_api_key:
        return "Please provide a Google API key to generate a summary."
    
    try:
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.5)
        
        # Split text if it's too long
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=8000,  # Gemini can handle larger chunks
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Process text in chunks if necessary
        chunks = text_splitter.split_text(text)
        
        if len(chunks) == 1:
            # For shorter texts, summarize directly
            prompt = f"Please summarize the following text extracted from a handwritten document. Focus on main points and organize them logically:\n\n{text}"
            summary = llm.invoke(prompt).content
            return summary
        else:
            # For longer texts, summarize each chunk and then combine
            chunk_summaries = []
            
            for i, chunk in enumerate(chunks):
                prompt = f"Please summarize this portion of text from a handwritten document:\n\n{chunk}"
                summary = llm.invoke(prompt).content
                chunk_summaries.append(summary)
            
            # Combine the chunk summaries
            combined_summary = "\n\n".join(chunk_summaries)
            
            # Generate a final summary of summaries
            final_prompt = f"Create a single cohesive summary from these section summaries of a handwritten document:\n\n{combined_summary}"
            final_summary = llm.invoke(final_prompt).content
            
            return final_summary
            
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# File upload section
st.header("Step 1: Upload PDF with Handwritten Content")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Process button
if uploaded_file is not None:
    if st.button("Process PDF"):
        with st.spinner("Extracting text from PDF..."):
            # Extract text
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.session_state.extracted_text = extracted_text
            
            # Generate summary if API key is provided
            if google_api_key:
                with st.spinner("Generating summary..."):
                    summary = generate_summary(extracted_text, google_api_key)
                    st.session_state.summary = summary
            else:
                st.session_state.summary = "Please provide a Google API key to generate a summary."
                
            st.session_state.processing_complete = True
            st.success("Processing complete!")

# Display results if processing is complete
if st.session_state.processing_complete:
    st.header("Step 2: Results")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Extracted Text", "Summary"])
    
    with tab1:
        st.subheader("Extracted Text")
        st.text_area("", st.session_state.extracted_text, height=400)
        
        # Download button for extracted text
        if st.session_state.extracted_text:
            text_bytes = st.session_state.extracted_text.encode()
            st.download_button(
                label="Download Extracted Text",
                data=text_bytes,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
    
    with tab2:
        st.subheader("AI-Generated Summary")
        if not google_api_key:
            st.warning("Please enter your Google API key in the sidebar to generate a summary.")
        else:
            st.markdown(st.session_state.summary)
            
            # Download button for summary
            if st.session_state.summary and st.session_state.summary != "Please provide a Google API key to generate a summary.":
                summary_bytes = st.session_state.summary.encode()
                st.download_button(
                    label="Download Summary",
                    data=summary_bytes,
                    file_name="summary.txt",
                    mime="text/plain"
                )
