import nltk
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

from nltk import word_tokenize, sent_tokenize

from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer

import string

import streamlit as st

# Load the text file and preprocess the data

with open('nlp_knowledge_base.txt', 'r', encoding='utf-8') as f:

    data = f.read().replace('\n', ' ')

# Tokenize the text into sentences

sentences = sent_tokenize(data)

# Define a function to preprocess each sentence

# Define a function to preprocess each sentence

def preprocess(sentence):
    # Tokenize the sentence into words
    words = word_tokenize(sentence)
    # Remove stopwords and punctuation
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Preprocess each sentence in the text
corpus = [preprocess(sentence) for sentence in sentences]

# Define a function to find the most relevant sentence given a query

def get_most_relevant_sentence(query):

    # Preprocess the query

    query = preprocess(query)

    # Compute the similarity between the query and each sentence in the text

    max_similarity = 0

    most_relevant_sentence = ""

    for sentence in corpus:

        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))

        if similarity > max_similarity:

            max_similarity = similarity

            most_relevant_sentence = " ".join(sentence)

    return most_relevant_sentence

def chatbot(question):

    # Find the most relevant sentence

    most_relevant_sentence = get_most_relevant_sentence(question)

    # Return the answer

    return most_relevant_sentence

def main():

    st.title("Isaac's Chatbot")

    st.write("Ask me anything about Isaac!")

    # Input box for user question

    question = st.text_input("Your question:")

    if st.button("Submit"):
        response = chatbot(question)
        st.write("Answer:", response)

if __name__ == "__main__":
    main()