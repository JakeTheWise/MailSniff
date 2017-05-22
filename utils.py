from bs4 import BeautifulSoup as BS
from bs4 import Comment
import base64
import pandas as pd
import numpy as np
import datetime as dt
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
from ticktock import tick, tock

def getBody(payload):
    '''Recursively hunts for and decodes the raw message body data.
    Handles the following MIME types that the Gmail API returns:
        text/plain, text/html, multipart/alternative, multipart/mixed 
    Returns English.'''
    mimeType = payload['mimeType']
    if mimeType == 'text/plain' and 'data' in payload['body']:
        return " ".join(base64.urlsafe_b64decode(payload['body']['data'].encode('UTF-8')).decode('UTF-8').splitlines())
    elif mimeType == 'text/html' and 'data' in payload['body']:
        soup = BS(payload['body']['data'], 'html.parser')
        for comment in soup.findAll(t=lambda text: isinstance(t, Comment)):
            comment.extract()
        return soup.get_text()
    elif 'parts' in payload:
        for part in payload['parts']:
            text = getBody(part)
            if text:
                return text
                
def jsonList2DF(msgList):
    '''Converts raw message data (as a List of Gmail API JSON responses) 
    to a pandas dataframe with subject, date, and message body.
    Indexed by unique message ID.'''
    data = {}
    count = 0
    print(len(msgList))
    for msg in msgList:
        d = {}
        for header in msg['payload']['headers']:
            if header['name'] == 'From':
                d['from'] = header['value']
            if header['name'] == 'Subject':
                d['subject'] = header['value']

        d['body'] = getBody(msg['payload'])
        d['date'] = dt.datetime.fromtimestamp(int(msg['internalDate']) / 1e3)
        data[msg['id']] = d
        count += 1
        if count % 2000 == 0:
            tock(float(count)/len(msgList))
    return pd.DataFrame(data).transpose()
