import sys
import re
import preprocessor as p
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import emoji
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()	
# pylint: disable=no-member
p.set_options(p.OPT.URL,p.OPT.SMILEY)
stop_words =  stopwords.words('english')
# Remove slogans and popular hashtags that don't mean much
stop_words.extend(['getahead','chooseforward','missionpossible','forwardtogether','initforyou','notasadvertised','elxn43','cdnpoli','ppc','gpc','ppc2019','peoplespca'])
# Remove party names - hard to know whether to remove words like "liberal" or "green" as they are often used in other contexts
stop_words.extend(['elxn43','cdnpoli','ppc','ndp','gpc','pcs','ppc2019','peoplespca'])
stop_words.extend(['get','dont','let','&amp;','amp','canadian']) #some words that aren't in the stopwords list but seem like they should be

def clean_text(sentence):
        sentence = sentence.lower()
        sentence = p.clean(sentence)
        sentence = emoji.demojize(sentence)
        token_words=word_tokenize(sentence)
        token_words
        stem_sentence=[]
        for token in token_words:
            token = re.sub("[,\.!?']", '', token)
            token = lemmatizer.lemmatize(token)
            if token not in stop_words and len(token) >= 3:
                stem_sentence.append(token)
                stem_sentence.append(" ")
        return "".join(stem_sentence)

if __name__ == "__main__":
    # This is a quick and dirty way to take in already outputted csvs and re-clean the text.
    usernames = sys.argv[1:]
    file_path = "../data/{}_data.csv"
    for username in usernames:
        twitter_df = pd.read_csv(file_path.format(username))
        new_clean = twitter_df["original_text"]
        print("--- cleaning text ---")
        new_clean = new_clean.apply(clean_text)
        twitter_df["clean_text"] = new_clean
        print("--- writing {} to file ---".format(username))
        csvFile = open(file_path.format(username), 'w' ,encoding='utf-8')
        twitter_df.to_csv(csvFile, mode='w', index=False, encoding="utf-8")

