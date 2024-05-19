from flask import Flask, request, render_template
from newspaper import Article
from bs4 import BeautifulSoup
from summa.summarizer import summarize as textrank_summarize
import nltk
import re
import string

nltk.download('punkt')

def remove_non_ascii(text):
    return ''.join(char if char in string.printable else ' ' for char in text)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    comparison = ''
    title = ''

    if request.method == 'POST':
        url = request.form['url']

        try:
            article = Article(url)
            article.download()
            article.parse()

            title = article.title
            
            #Lowercasing
            soup = BeautifulSoup(article.html, 'html.parser')
            article_text = ' '.join([p.get_text() for p in soup.find_all('p')])

            
             # Menghilangkan tanda baca
            article_text = re.sub(r'[^\w\s]', '', article_text)

            
            # Menggunakan TextRank untuk meringkas
            textrank_summary = textrank_summarize(article_text, ratio=0.2)


            # Tokenisasi
            original_sentences = nltk.sent_tokenize(article_text)
            num_original_sentences = len(original_sentences)

            textrank_summary_sentences = nltk.sent_tokenize(textrank_summary)
            num_textrank_summary_sentences = len(textrank_summary_sentences)

            summary = textrank_summary
            comparison = f"{num_textrank_summary_sentences} / {num_original_sentences} = {num_textrank_summary_sentences / num_original_sentences}"

        except Exception as e:
            summary = f"Error: {str(e)}"

    return render_template('index.html', title=title, summary=summary, comparison=comparison)

if __name__ == '__main__':
    app.run(debug=True)
