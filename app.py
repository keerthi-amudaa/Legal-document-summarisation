import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from googletrans import Translator
import fitz  # PyMuPDF for PDF text extraction
import re
from gtts import gTTS
import os

# Initialize and cache model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("nsi319/legal-led-base-16384")
    model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-led-base-16384")
    return tokenizer, model

tokenizer, model = load_model()

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            pdf_text += page.get_text("text")
    return pdf_text

# Format and clean up summary
def format_summary(text):
    text = re.sub(r"[^a-zA-Z0-9\s.,;:!?-]", "", text)  # Clean text
    sentences = text.split(". ")
    formatted_summary = ""
    for i, sentence in enumerate(sentences):
        if i % 3 == 0:  # Paragraph every 3 sentences
            formatted_summary += f"\n\n{sentence.strip()}."
        else:
            formatted_summary += f"\n• **{sentence.strip()}**."
    return formatted_summary

# Summarize text
def summarize_text(text, max_input_length=6144, min_summary_length=350, max_summary_length=500):
    input_tokenized = tokenizer.encode(
        text, return_tensors='pt', padding="max_length", 
        pad_to_max_length=True, max_length=max_input_length, truncation=True
    )
    
    summary_ids = model.generate(
        input_tokenized,
        num_beams=4,
        no_repeat_ngram_size=3,
        length_penalty=2.0,
        min_length=min_summary_length,
        max_length=max_summary_length
    )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return format_summary(summary)

# Text-to-Speech function
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_file = 'translated_audio.mp3'
    tts.save(audio_file)
    return audio_file

# Language codes for translation
lang_codes = {
    "Hindi": "hi",
    "Kannada": "kn",
    "Telugu": "te",
    "Tamil": "ta",
    "Malayalam": "ml"
}

# Streamlit Layout
st.markdown(
    "<h1 style='text-align: center; color: #3c6e71;'>BrevityLaw</h1>"
    "<h4 style='text-align: center; color: #283d3b;'>Bringing simplicity to legal documents</h4>",
    unsafe_allow_html=True
)
st.write("---")

# Upload section
st.markdown(
    "<div style='background-color: #d9e8e4; padding: 10px; border-radius: 5px;'>"
    "<h3 style='text-align: center;'>Upload Your PDF Document</h3>"
    "</div>", unsafe_allow_html=True
)

pdf_file = st.file_uploader("Choose a document", type="pdf", label_visibility="collapsed")

# Initialize session state variables
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if pdf_file is not None:
    with st.spinner("Extracting text from PDF..."):
        st.session_state.extracted_text = extract_text_from_pdf(pdf_file)
    
    if st.button("Summarize Text"):
        with st.spinner("Generating summary..."):
            st.session_state.summary = summarize_text(st.session_state.extracted_text)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<h3 style='text-align: center; color: #3c6e71;'>Extracted Text</h3>", unsafe_allow_html=True)
        st.text_area("", st.session_state.extracted_text, height=400, key="extracted_text_display")

    with col2:
        st.markdown("<h3 style='text-align: center; color: #3c6e71;'>Summarized Text</h3>", unsafe_allow_html=True)
        st.text_area("", st.session_state.summary, height=400, key="summarized_text_display")

    st.write("---")
    st.markdown("<h3 style='text-align: center; color: #3c6e71;'>Translate Summary</h3>", unsafe_allow_html=True)

    selected_language = st.selectbox(
        "Choose a language", list(lang_codes.keys()), key="language"
    )

    if st.button("Translate"):
        translator = Translator()
        
        with st.spinner("🔄 Translating..."):
            try:
                translation = translator.translate(st.session_state.summary, dest=lang_codes[selected_language])
                st.session_state.translated_text = translation.text
            except Exception as e:
                st.session_state.translated_text = f"Translation error: {e}"

    if st.session_state.translated_text:
        st.markdown("<h3 style='text-align: center; color: #3c6e71;'>Translated Text</h3>", unsafe_allow_html=True)
        st.text_area("", st.session_state.translated_text, height=200, key="translated_text_display")

        # Text-to-Speech Button
        if st.button("Convert to Speech"):
            audio_file = text_to_speech(st.session_state.translated_text, lang=lang_codes[selected_language])
            st.success("Audio generated successfully!")

            # Play the audio in Streamlit
            st.audio(audio_file)

else:
    st.info("Please upload a PDF file to begin.")

# Footer
st.markdown("<hr style='border:1px solid #3c6e71;'>", unsafe_allow_html=True)
st.caption("© BrevityLaw - Bringing simplicity to legal documents")
