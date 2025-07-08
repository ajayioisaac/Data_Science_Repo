import streamlit as st
import speech_recognition as sr
import nltk
import string
import random
import time

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# NLTK setup
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# --- Load Placeholder Knowledge Base ---
try:
    with open('nlp_knowledge_base.txt', 'r', encoding='utf-8') as f:
        corpus = f.read()
except FileNotFoundError:
    corpus = """
    Natural language processing is a subfield of artificial intelligence.
    NLP enables computers to understand, interpret, and generate human language.
    Speech recognition converts spoken words into text.
    A chatbot is a computer program that simulates human conversation.
    """

sentences = sent_tokenize(corpus.lower())


# --- Preprocess User Input and Knowledge Base ---
def clean_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)


# --- Match Response using TF-IDF + Cosine Similarity ---
def get_chatbot_response(user_input):
    cleaned_input = clean_text(user_input)
    all_sentences = sentences + [cleaned_input]

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(all_sentences)
    similarity = cosine_similarity(tfidf[-1], tfidf[:-1])

    idx = similarity.argmax()
    score = similarity[0, idx]

    if score > 0.2:
        return sentences[idx].capitalize()
    else:
        return "I’m not sure how to respond to that."


# Speech recognition function
def transcribe_speech(language='en-US'):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    try:
        text = recognizer.recognize_google(audio, language=language)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        st.error(f"Request failed: {e}")
    return ""

# --- Streamlit UI ---
st.set_page_config(page_title="Speech-Enabled Chatbot")
st.title("🤖 Speech-Enabled Chatbot")

st.markdown("This chatbot pulls responses from a knowledge base file using NLP similarity matching.")

mode = st.radio("Select input method:", ["Text", "Voice"])
user_input = ""

if mode == "Text":
    user_input = st.text_input("💬 Type your message:")
elif mode == "Voice":
    if st.button("🎤 Start Listening"):
        user_input = transcribe_speech()

# --- Generate Response ---
if user_input:
    response = get_chatbot_response(user_input)
    st.markdown(f"**🤖 Bot:** {response}")
