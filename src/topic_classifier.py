class TopicClassifier():

    """ Class constructor """
    def __init__(self):
        pass

    """ Classifies a news topic according the the macro-topics EconomicsTopics and OtherTopics, and the specific
    economics topics CompaniesEconomy, Markets&Goods, NationalEconomy
    @:param news title of the news to classify
    @:return tuple indicating the specific topic of the news and the macro-topic """
    def classify_news(self, news: str) -> tuple:
        return 'EconomicsTopics', 'CompaniesEconomy'
