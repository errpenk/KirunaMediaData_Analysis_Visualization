# Strategies for Handling Long Texts: 
# For long text content such as articles and reports, sentence segmentation techniques are used for analysis

from nltk.tokenize import sent_tokenize
 
long_text = "THIS IS A LONG TEXT"
 
sentences = sent_tokenize(long_text)
for sentence in sentences:
    vs = analyzer.polarity_scores(sentence)
    print(f"SENTENCE：{sentence}")
    print(f"SCORE：{vs['compound']:.2f}")
