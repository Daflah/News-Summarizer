import re
import nltk
import string
from summa.summarizer import summarize as textrank_summarize
from newspaper import Article
from bs4 import BeautifulSoup

nltk.download('punkt')

def remove_non_ascii(text):
    return ''.join(char if char in string.printable else ' ' for char in text)

# Meminta pengguna untuk memasukkan URL berita
url = input("Masukkan URL berita: ")

# Mengunduh dan memproses artikel dari URL
article = Article(url)
article.download()
article.parse()

# Mendapatkan judul artikel
article_title = article.title

# Melakukan pemrosesan NLP untuk artikel
article.nlp()

# Mendapatkan teks dari artikel
soup = BeautifulSoup(article.html, 'html.parser')
article_text = ' '.join([p.get_text() for p in soup.find_all('p')])  # Mengambil teks dari paragraf

# Mengenali tanda baca
article_text = re.sub(r'[^\w\s]', '', article_text)  # Menghapus karakter non-ASCII dan tanda baca

# Melakukan rangkuman menggunakan Summa (TextRank)
textrank_summary = textrank_summarize(article_text, ratio=0.2)  # Ubah ratio sesuai kebutuhan

# Hitung jumlah kalimat dalam teks asli
original_sentences = nltk.sent_tokenize(article_text)
num_original_sentences = len(original_sentences)

# Hitung jumlah kalimat dalam ringkasan (TextRank)
textrank_summary_sentences = nltk.sent_tokenize(textrank_summary)
num_textrank_summary_sentences = len(textrank_summary_sentences)

print(f'Title: {article_title}')
print(f'Textrank Summary: {textrank_summary}')

# Perbandingan jumlah kalimat
print(f"Perbandingan jumlah kalimat (TextRank): {num_textrank_summary_sentences} / {num_original_sentences} = {num_textrank_summary_sentences / num_original_sentences}")