from time import time
starttime = time()
#import sys
import re
import matplotlib.pyplot as plt
#import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiment_analyzer = SentimentIntensityAnalyzer()


mediaPattern = r"(\<Media omitted\>)" # Because it serves no purpose
regexMedia = re.compile(mediaPattern, flags=re.M)

dateAndTimepattern = r"(\d+\/\d+\/\d+)(,)(\s)(\d+:\d+)(\s)(\w+)(\s)(-)(\s\w+)*(:)"
regexDate = re.compile(dateAndTimepattern, flags=re.M)

def cleanText(filename):    
    chat = open(filename,encoding="utf-8")
    chatText = chat.read()
    chat.close()

 
    chatText = regexMedia.sub("", chatText)
    chatText = regexDate.sub("", chatText)

    lines = []

    for line in chatText.splitlines():
        if line.strip() is not "": # If it's empty, we don't need it
            lines.append(line.strip())

    return lines
def analyze(name):
    linesList = cleanText(name + '.txt')
    neutral, negative, positive = 0, 0, 0

    for index, sentence in enumerate(linesList):
        # print("Processing {0}%".format(str((index * 100) / len(linesList))))
        
        if re.match(r'^[\w]', sentence) is None:
            continue
        scores = sentiment_analyzer.polarity_scores(sentence)
        scores.pop('compound', None)

        maxAttribute = max(scores, key=lambda k: scores[k])

        if maxAttribute == "neu":
            neutral += 1
        elif maxAttribute == "neg":
            negative += 1
        else:
            positive += 1

    total = neutral + negative + positive
    print("Negative: {0}% | Neutral: {1}% | Positive: {2}%".format(
        negative*100/total, neutral*100/total, positive*100/total))

    labels = 'Neutral', 'Negative', 'Positive'
    sizes = [neutral, negative, positive]
    colors = ['#00bcd7', '#F57C00', '#CDDC39']

     # Plot
    plt.pie(sizes, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=140)

    plt.axis('equal')
    plt.title("Sentiment Analysis - Chat with {0}".format(name.capitalize()))
    plt.show()	


   
analyze("chat_sam")
endtime = time()
elapsed = endtime - starttime
print(elapsed)
