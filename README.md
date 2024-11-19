# **BrevityLaw - Legal Document Summarization**

**BrevityLaw** is an AI-powered web application designed to simplify and summarize complex legal documents. By leveraging natural language processing (NLP) models, this tool extracts key information from lengthy legal PDFs, generates concise summaries, and supports multilingual translations. Additionally, it offers the functionality to convert the summary to speech, making legal information more accessible to a wider audience.

---

## **Features**

- **PDF Upload**: Upload your legal documents in PDF format.
- **Text Extraction**: Extracts text from PDF documents using PyMuPDF (fitz).
- **Text Summarization**: Generate concise summaries using the `legal-led-base-16384` deep learning model.
- **Translation**: Translate summaries into various languages such as Hindi, Kannada, Telugu, Tamil, and Malayalam.
- **Text-to-Speech**: Convert the summarized or translated text into audio for better accessibility.

---

## **Technologies**

- **Streamlit**: Python framework for creating interactive web applications.
- **Transformers (Hugging Face)**: Pre-trained models for natural language processing (NLP), specifically the `legal-led-base-16384` for legal document summarization.
- **PyMuPDF (fitz)**: For extracting text from PDF files.
- **Google Translate API**: For translating the text into multiple languages.
- **gTTS (Google Text-to-Speech)**: Converts text into speech (audio format).

---

## **Setup and Installation**

## Getting Started

To get started with the BrevityLaw, you need to:

1. **Clone the repository**:
  ```bash
git clone https://github.com/keerthi-amudaa/Legal-document-summarisation.git
cd Legal-document-summarisation
```


2. **Install the required dependencies**:
  ```bash
  pip install -r requirements.txt
  ```
    


3. Download the `legal-led-base-16384`model from Hugging face [here](https://huggingface.co/nsi319/legal-led-base-16384)



4. **Run the Streamlit app**
```bash
streamlit run app.py
```
This will start the Streamlit server and open the web application in your browser.



## Usage

1. **Upload a Legal Document**: Click on the Upload button and select a PDF document containing the legal text.
   
2. **Summarize**: After the text is extracted, click the Summarize Text button to generate a concise summary.

3. **Translate**: Choose the desired language from the dropdown and click Translate to convert the summary into that language.

4. **Text-to-Speech**: Click Convert to Speech to hear the translated summary.

## Contributing

Contributions to the BrevityLaw are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository to your own GitHub account.

2. Create a new branch for your feature or bug fix.

3. Make your changes and ensure that the code passes all tests.

4. Create a pull request to the main repository, explaining your changes and improvements.

5. Your pull request will be reviewed, and if approved, it will be merged into the main codebase.

## License

This project is licensed under the MIT License.

---






**BrevityLaw - Simplifying Legal Documents**

