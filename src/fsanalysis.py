import pandas as pd
import csv
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

'''
This class is for sentiment analysis of financial text
'''


class FinancialSentimentAnalysis:

    def __init__(self):
        # nltk.downloader.download('vader_lexicon')
        # nltk.download('wordnet')
        # nltk.download('stopwords')
        self.sia = SentimentIntensityAnalyzer()

        # Since SentimentIntensityAnalyzer does not contain financial terms
        # is needed to provide them. Files are hosted in './lexicon_data' folder

        # # # stock market lexicon
        stock_lex = pd.read_csv('lexicon_data/stock_lex.csv')
        stock_lex['sentiment'] = (stock_lex['Aff_Score'] + stock_lex['Neg_Score']) / 2
        stock_lex = dict(zip(stock_lex.Item, stock_lex.sentiment))
        stock_lex = {k: v for k, v in stock_lex.items() if len(k.split(' ')) == 1}
        stock_lex_scaled = {}
        for k, v in stock_lex.items():
            if v > 0:
                stock_lex_scaled[k] = v / max(stock_lex.values()) * 4
            else:
                stock_lex_scaled[k] = v / min(stock_lex.values()) * -4

        # # # Loughran and McDonald financial lexicon
        positive = []
        with open('lexicon_data/lm_positive.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                positive.append(row[0].strip())

        negative = []
        with open('lexicon_data/lm_negative.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                entry = row[0].strip().split(" ")
                if len(entry) > 1:
                    negative.extend(entry)
                else:
                    negative.append(entry[0])

        final_lex = {}
        final_lex.update({word: 2.0 for word in positive})
        final_lex.update({word: -2.0 for word in negative})
        final_lex.update(stock_lex_scaled)
        final_lex.update(self.sia.lexicon)
        self.sia.lexicon = final_lex

    def sentiment_analysis(self, t: str) -> str:
        t = t.lower()  # Get the news headline

        # Tokenization
        tokenizer = RegexpTokenizer(r'\w+')  # Take only words from sentence
        tokens = tokenizer.tokenize(t)

        # Lemmatization
        lemmatizer = WordNetLemmatizer()  # From words takes only Lemmas. e.g.: raises -> raise
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

        # Stop words
        stopwords = nltk.corpus.stopwords.words('english')  # Remove english stopword. e.g.: 'on','at' ecc.
        # print(stopwords) #print for more
        tokens_new = [j for j in tokens if j not in stopwords]

        ss = self.sia.polarity_scores(t)  # Compute polarity of the sentence. Compound is the threshold

        # print("Scores: ", end='')
        # for k in sorted(ss):
        #    print('{0}: {1}, '.format(k, ss[k]), end='')
        # print()

        return str(ss[sorted(ss)[0]])


if __name__ == "__main__":
    fsa = FinancialSentimentAnalysis()
    result = fsa.sentiment_analysis('Singapore Growth to Remain Weak Amid Global Risks, IMF Says')
    print(result)
