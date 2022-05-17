import logging


class QueryFilter(logging.Filter):

    def filter(self, record):
        try:
            return 'django_' not in record.args[1]
        except:
            return False
