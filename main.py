from tkinter import *
from tkinter import ttk
import nltk
import pandas as pd
from nltk.corpus import brown
from nltk.corpus import stopwords
from collections import Counter
import math

nltk.download('brown')
nltk.download('stopwords')

win = Tk()

win.title("TF-IDF Calculator")
win.geometry("750x250")

def calculate_tfidf():
   global entry
   document = entry.get()

   raw_text = ' '.join(brown.words(fileids=document))

   stop_words = set(stopwords.words('english'))
   tokens = nltk.word_tokenize(raw_text)
   tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]

   term_freq = Counter(tokens)

   corpus_freq = Counter()
   for fileid in brown.fileids():
       corpus_tokens = [token.lower() for token in brown.words(fileids=fileid) if
                        token.isalpha() and token.lower() not in stop_words]
       corpus_freq.update(set(corpus_tokens))

   inv_doc_freq = {}
   num_docs = len(brown.fileids())
   for term in term_freq:
       if corpus_freq[term] != 0:
           inv_doc_freq[term] = math.log(num_docs / corpus_freq[term])
       else:
           inv_doc_freq[term] = 0

   tf_idf = {}
   for term in term_freq:
       tf_idf[term] = term_freq[term] * inv_doc_freq[term]

   data = {'Term Frequency': term_freq, 'Document Frequency': corpus_freq, 'Inverse Document Frequency': inv_doc_freq,
           'TF-IDF': tf_idf}
   df = pd.DataFrame(data)

   with pd.ExcelWriter('tfidf.xlsx') as writer:
       df.to_excel(writer, sheet_name='Sheet1')


label = Label(win, text="Enter DocID:", font=("Courier 22 bold"))
label.pack()

entry = Entry(win, width=40)
entry.focus_set()
entry.pack()

ttk.Button(win, text="Calculate",width=20, command=calculate_tfidf).pack(pady=20)

win.mainloop()