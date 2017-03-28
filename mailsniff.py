from utils import jsonList2DF
import pickle

with open('messages.p','rb') as f:
    messages = pickle.load(f)

jsonList2DF(messages)

# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# stopWords = set(stopwords.words('english'))
# words = word_tokenize("".join(strings))
# wordsFiltered = []
# for w in words:
#     if w not in stopWords:
#         wordsFiltered.append(w)
 
# print(wordsFiltered)