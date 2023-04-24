#lib must install:
    # flask 
    # wikipedia 
    # pyarabic 
    # sumy or summa or gesmin || I used sumy 
#----------------------------------------

from flask import Flask ,render_template ,request
import wikipedia
#import summa
#from summa.summarizer import summarize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from pyarabic.araby import tokenize, is_arabicrange, strip_tashkeel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# summery fun
def summeryText(text , lang):
    parser = PlaintextParser.from_string(text,Tokenizer(lang))
    summarizer_4 = TextRankSummarizer()
    summary =summarizer_4(parser.document , 10)
    text_summary=""
    for sentence in summary:
        text_summary+=str(sentence)
    return text_summary

#clear english text ..
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return filtered_text


@app.route("/", methods=["GET" , "POST"])
def index():
    return render_template('index.html')

@app.route("/result", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        title = request.form.get("text")
        sel = request.form.get("sel")
        wikipedia.set_lang(sel)
        text=wikipedia.page(title).content
        if sel == 'ar':
            finalText = summeryText(text,'arabic')
            arabic = tokenize(finalText,conditions=is_arabicrange,morphs=strip_tashkeel)
            arabicText = " ".join(arabic)
            return render_template('content.html',data=text,title=title,summerize=arabicText,s=sel)
        else :
            text = summeryText(text,'english')
            finalText = remove_stopwords(text)
            finalText = " ".join(finalText)
            return render_template('engContent.html',data=text,summerize=finalText)
    return render_template('content.html')

if __name__ == "__main__":
    app.run(debug=True)

