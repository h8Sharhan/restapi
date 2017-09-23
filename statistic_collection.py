from operator import itemgetter


class StatisticCollection:
    def __init__(self):
        self._collection_dict = {}

    def save_to_collection(self, word):
        word = word.lower()
        if word in self._collection_dict:
            self._collection_dict[word] += 1
        else:
            self._collection_dict[word] = 1

    def get_most_popular(self, number):
        return dict(sorted(self._collection_dict.iteritems(), key=itemgetter(1), reverse=True)[:number])


if __name__ == '__main__':
    pass