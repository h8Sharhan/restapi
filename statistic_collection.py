import logging
from operator import itemgetter
from os.path import exists
from yaml import dump, load

logger = logging.getLogger(__name__)


class StatisticCollection(object):
    def __init__(self):
        self.file_name = 'collection.yaml'
        # Initialize dict
        self._statistic_dict = {}
        if exists(self.file_name):
            self._load_collection_from_file()

    def __del__(self):
        self._save_collection_to_file()

    def _save_collection_to_file(self):
        logger.info('Save collection to file %s' % self.file_name)
        with open(self.file_name, 'w+') as yaml_stor:
            dump(self._statistic_dict, yaml_stor, default_flow_style=False)

    def _load_collection_from_file(self):
        logger.info('Load collection from file %s' % self.file_name)
        with open(self.file_name, 'r') as yaml_stor:
            self._statistic_dict = load(yaml_stor)

    def save(self, word):
        word = word.lower()
        if word not in self._statistic_dict:
            self._statistic_dict[word] = 1
        else:
            self._statistic_dict[word] += 1

    def get_most_popular(self, number):
        # If collection statistic is empty list of popular will be empty too
        if self._statistic_dict:
            return [k for k, v in sorted(self._statistic_dict.iteritems(), key=itemgetter(1), reverse=True)[:number]]


if __name__ == '__main__':
    test_collection = StatisticCollection()
    test_collection.save('Ninja')
    print test_collection.get_most_popular(2)
