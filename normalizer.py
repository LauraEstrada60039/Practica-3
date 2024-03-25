
import re
import spacy
from spacy import displacy
import pandas as pd
import re
from datetime import datetime
INPUT_FILE = "corpus_raw.csv"
OUTPUT_FILE = "corpus_normalized.csv"
# Load the Spanish language model
nlp = spacy.load("es_core_news_sm")

# Define stop words list, it should include articles, prepositions, conjunctions and pronouns in spanish

stop_words = set(["a", "ante", "antes", "bajo", "cabe", "con", "contra", "de", "desde", "después",
                "durante", "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según",
                "sin", "so", "sobre", "tras", "versus", "vía", "y", "yo", "él", "ella", "ello",
                "nosotros", "nosotras", "vosotros", "vosotras", "ustedes", "ellos", "ellas",
                "este", "esta", "esto", "esos", "esas", "aquel", "aquella", "aquello", "aquellos",
                "aquellas", "le", "les", "me", "nos", "se", "te", "lo", "la", "los", "las", "un", "una",
                "unos", "unas", "uno", "pero", "porque", "si", "no", "ni", "o", "u", "mas", "menos",
                "e", "i", "ya", "que", "también", "tampoco", "al", "del", "el", "las", "los", "su", "tus"])

# Additional function to identify grammatical categories
def is_grammatical_category(token):
    return token.pos_ in {"DET", "ADP", "SCONJ", "PRON"}

# Function to normalize a text string
def normalize_text(text):
    # Tokenize the text
    tokens = nlp(text)

    # Remove stop words and tokens from specific grammatical categories
    filtered_tokens = [token for token in tokens if (token.text not in stop_words) and not is_grammatical_category(token)]

    # Lemmatize the tokens
    lemmas = [token.lemma_ for token in filtered_tokens]

    # Join the normalized tokens as a string
    normalized_text = " ".join(lemmas)

    return normalized_text

def month2num(month_str):
    # Dictionary to map month names to their corresponding number
    month_map = {"ene": "01","feb": "02","mar": "03",
                 "abr": "04","may": "05","jun": "06",
                 "jul": "07","ago": "08","sep": "09",
                 "oct": "10","nov": "11", "dic": "12"
                }

    # Return the corresponding number for the input month name
    return month_map[month_str.lower()]

num = ["0","1","2","3","4","5","6","7","8","9"]

def parse_date(date_str):
    # Regular expression pattern to match the expected date format
    pattern = r"^\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} \w{3}$"
    try:
        # If the input string matches the expected format, parse it as a date and return it in the DD/MM/YYYY format
        a = 0
        for i in num:
            if i in date_str:
                a = 1
        if a == 0: return date_str
        
        date = date_str[5:16]
        day = date[0:2]
        month = month2num(date[3:6])
        year = date[7:11]
        date_formatted = f"{day}/{month}/{year}"
        return date_formatted
    except ValueError:
     # If the input string doesn't match the expected format, return the original string
        return date_str

def normalize_corpus(INPUT_FILE, OUTPUT_FILE):
    # Read the data corpus as a pandas DataFrame
    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        # Group the strings between quotes as a single column so the commas inside the quotes are not interpreted as column separators
        pattern = r'"([^"]*)"'
        entries = []

        for entry in file:
            entry_data = re.split(r',\s*(?=(?:[^"]*"[^"]*")*[^"]*$)', entry)
            entry_data = [re.sub(pattern, r'\1', value).strip('" ') for value in entry_data]
            entries.append(entry_data)

        corpus_raw = pd.DataFrame(entries)
        
        corpus_normalized = corpus_raw.copy() 
        #Ignore the first row, it's the header
        #We normalize the title and content columns, and the date it's change to DD/MM/YYYY format
    
        corpus_normalized[1] = corpus_normalized[1].apply(normalize_text)
        corpus_normalized[2] = corpus_normalized[2].apply(normalize_text)
        corpus_normalized[5] = corpus_normalized[5].apply(parse_date)
        
        

    # Write the normalized data corpus to the output file
    corpus_normalized.to_csv(OUTPUT_FILE, index=False, header=False)

    # Save the normalized data to a new CSV file
