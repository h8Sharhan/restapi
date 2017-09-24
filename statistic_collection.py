from operator import itemgetter


class StatisticCollection:
    def __init__(self):
        # self._statistic_dict = {}
        # Initialise with data for testing purposes
        self._statistic_dict = {'ninja': 73, 'jedi': 14, 'cruiser': 153, 'destroyer': 25, 'battleship': 73}

    def save(self, word):
        word = word.lower()
        if word not in self._statistic_dict:
            self._statistic_dict[word] = 1
        else:
            self._statistic_dict[word] += 1

    def get_most_popular(self, number):
        if self._statistic_dict:
            return [k for k, v in sorted(self._statistic_dict.iteritems(), key=itemgetter(1), reverse=True)[:number]]


if __name__ == '__main__':
    test_collection = StatisticCollection()
    test_collection.save('Ninja')
    print test_collection.get_most_popular(2)
