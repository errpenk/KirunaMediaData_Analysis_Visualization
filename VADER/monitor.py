# Batch analysis of user comment sentiment
comments = [
    "good",
    "normal",
    "bad"
]
 
for comment in comments:
    score = analyzer.polarity_scores(comment)
    compound = score['compound']
    
    if compound >= 0.05:
        sentiment = "pos"
    elif compound <= -0.05:
        sentiment = "neg"
    else:
        sentiment = "neu"
    
    print(f"COMMENT：{comment}")
    print(f"Emotional Tendency：{sentiment}（Overall score：{compound:.2f}）")
