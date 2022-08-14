import csv
import datetime
import os

def logger(path):
    def _logger(smth_old):
        def smth_new(*args, **kwargs):
            new_list = []
            result = smth_old(*args, **kwargs)
            if args and kwargs:
                argums = args, kwargs
            elif args:
                argums = args
            else:
                argums = kwargs
            new_list.extend([datetime.datetime.now().strftime('%c'), smth_old.__name__, argums, result])
            with open(os.path.join(path, 'logs.csv'), 'a', encoding='utf-8') as f:
                datawriter = csv.writer(f)
                datawriter.writerow(new_list)

            return result
        return smth_new
    return _logger


if __name__ == '__main__':
    pass
