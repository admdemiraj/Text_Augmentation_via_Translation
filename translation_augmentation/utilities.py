import os
import pickle


def file_cache_name(file):
    head, tail = os.path.split(file)
    filename, ext = os.path.splitext(tail)
    return os.path.join(head, filename + ".p")


def write_cache_translation(file, data):
    with open(file_cache_name(file), 'wb') as pickle_file:
        pickle.dump(data, pickle_file)


def load_cache_translation(file):
    with open(file_cache_name(file), 'rb') as f:
        return pickle.load(f)

