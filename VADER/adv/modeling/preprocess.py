import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# read
df = pd.read_csv('imdb_reviews.csv')

# clean
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
    return ' '.join(tokens)

df['ProcessedReview'] = df['Review'].apply(preprocess_text)
print(df.head())
