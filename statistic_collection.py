import yaml
from operator import itemgetter
from os.path import exists


class StatisticCollection(object):
    def __init__(self):
        self.file_name = 'collection.yaml'
        # Initialize dict
        self._statistic_dict = {}
        if exists(self.file_name):
            with open(self.file_name, 'r') as yaml_stor:
                self._statistic_dict = yaml.load(yaml_stor)

    def save(self, word):
        word = word.lower()
        if word not in self._statistic_dict:
            self._statistic_dict[word] = 1
        else:
            self._statistic_dict[word] += 1

    def get_most_popular(self, number):
        if self._statistic_dict:
            return [k for k, v in sorted(self._statistic_dict.iteritems(), key=itemgetter(1), reverse=True)[:number]]

    def save_stor_to_file(self):
        with open(self.file_name, 'w+') as yaml_stor:
            yaml.dump( self._statistic_dict, yaml_stor, default_flow_style=False)


if __name__ == '__main__':
    test_collection = StatisticCollection()
    test_collection.save('Ninja')
    test_collection.save_stor_to_file()
    print test_collection.get_most_popular(2)
