from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Calculate the sentiment score for each review
df['SentimentScore'] = df['ProcessedReview'].apply(lambda x: sid.polarity_scores(x)['compound'])

# Categorize reviews based on their sentiment scores
df['Sentiment'] = df['SentimentScore'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))

print(df.head())
