from textblob import TextBlob

def fix_spelling(text):
    output = str(TextBlob(text).correct())
    return output