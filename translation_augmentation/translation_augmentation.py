from googletrans import Translator
from translation_augmentation.utilities import load_cache_translation, write_cache_translation
import os, sys
import numpy as np

__name__ = "translation_augmentation"


def determine_path():
    try:
        root = __file__
        if os.path.islink(root):
            root = os.path.realpath(root)
        return os.path.dirname(os.path.abspath(root))

    except:
        print("I'm sorry, but something is wrong.")
        print("There is no __file__ variable. Please contact the author.")
        sys.exit()


def start():
    print("module is running")
    print(determine_path())
    print("My various data files and so on are:")
    files = [f for f in os.listdir(determine_path() + "/things")]
    print(files)


if __name__ == "__main__":
    print("Decide what to do")

def translate_single(text, dest, src):
    translator = Translator()
    result1 = translator.translate(text, dest=dest, src=src)
    result2 = translator.translate(result1.text, dest=src, src=dest)
    return str(result2.text)

def translate_double(text, dest, src):
    translator = Translator()
    result1 = translator.translate(text, dest=dest, src=src)
    result2 = translator.translate(result1.text, dest='de', src=dest)
    result3 = translator.translate(result2.text, dest=src, src='de')
    return str(result3.text)

def augment_data_simple(text, times, strategy="single",src="en"):
    '''
    This is a method that does text augmentation by translating the
    given text in another language and then translating it back in
    the original one. The text will have changed a bit
    (it will be different) but hopefully similar with the original
     text. Given X_train we return the new X_train with the augmented data.
    :param text:
    :param times:
    :param strategy:
    :param src:
    :return:(X_train augmented)
    text            --> (X_train original) the text we want to augment (and array of sentences)
    times           --> how many times we want to augment each given sentense (up to 3 because
                        we get good translations only between the languages: English,Spanish,German,French)
    strategy        --> single : translate from the original language to another and back to the original
                                 e.g. EN to DE to EN
                        double : translate from the original language to 2 other languages and back to the original
                                 e.g. EN to DE to SP to EN
    src             --> in which language the initial text is in.Possible options 'en','de','es','fr'

    !!Note!! A folder named 'Translation' is created in the current working directory and the translation is saved
    there in a file named 'translation_simple.p'. If you re-run this method the translation will be loaded from that
    file in order to save time. If you want to make a new translation each time simply delete the file 'translation_simple.p'.
    '''

    # in order to avoid this time consuming operation, cache the results
    file = os.getcwd() + "/Translation/translation_simple.p"
    # create a directory /home/name/Translation if it does not exist
    directory = os.getcwd() + "/Translation/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        print("Loading translation from cache. At directory: ", directory)
        cache = load_cache_translation(file)

        return cache
    except FileNotFoundError:
        print("Couldn't load translation from cache.")
        pass
    # X_train that will be returned
    return_sentences = np.array([])
    # all the available languages that we can make translations
    languages = ["en", "de", "fr", "es"]
    # remove the source language so it won't be used as a translation destination
    languages.remove(src)

    for idx, sent in enumerate(text):
        print(idx, sent)
        sent = str(sent)
        return_sentences = np.append(return_sentences, sent)

        for i in range(0, times):
            if strategy == "single":
                translation = translate_single(sent, languages[i], src)
                return_sentences = np.append(return_sentences, translation)
            elif strategy == "double":
                translation = translate_double(sent, languages[i], src)
                return_sentences = np.append(return_sentences, translation)

    # write the data to a cache file
    write_cache_translation(file, (return_sentences))
    return return_sentences


def augment_data(text, all_classes, classes_x_times, strategy="single", src="en"):
    '''
    This is a method that does text augmentation by translating the
    given text in another language and then translating it back in
    the original one. The text will have changed a bit
    (it will be different) but hopefully similar with the original
    text.Given X_train and y_train we return the new X_train with
    the augmented data and the new y_train.
    :param src:
    :param text:
    :param all_classes:
    :param classes_x_times:
    :param strategy:
    :return: return_sentences (X_train augmented), return_all_classes(y_train)
    text            --> (X_train original) the text we want to augment (and array of sentences)
    all_classes     --> (y_train) the classes that are present in each sentence
    classes_x_times --> dictionary containing the classes we want to augment
                        and how many times (up to 3 because we get good
                        translations only between the languages: English,Spanish,German,French)
    strategy        --> single : translate from the original language to another and back to the original
                                 e.g. EN to DE to EN
                        double : translate from the original language to 2 other languages and back to the original
                                 e.g. EN to DE to SP to EN
    src             --> in which language the initial text is in.Possible options 'en','de','es','fr'

    !!Note!! A folder named 'Translation' is created in the current working directory and the translation is saved
    there in a file named 'translation.p'. If you re-run this method the translation will be loaded from that
    file in order to save time. If you want to make a new translation each time simply delete the file 'translation.p'.

    '''

    # in order to avoid this time consuming operation, cache the results
    file = os.getcwd() + "/Translation/translation.p"
    # create a directory /home/name/Translation if it does not exist
    directory = os.getcwd() + "/Translation/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        print("Loading translation from cache. At directory: ", directory)
        cache = load_cache_translation(file)

        return cache
    except FileNotFoundError:
        print("Couldn't load translation from cache.")
        pass
    # X_train that will be returned
    return_sentences = np.array([])
    # y_train that will  be returned
    return_all_classes = []
    # all the available languages that we can make translations
    languages = ["en", "de", "fr", "es"]
    # remove the source language so it won't be used as a translation destination
    languages.remove(src)

    for idx, sent in enumerate(text):
        print(idx, sent)
        sent = str(sent)
        return_all_classes.append(all_classes[idx])
        return_sentences = np.append(return_sentences, sent)
        # find the position of the class that is present in the sentense
        category = (all_classes[idx] == 1).argmax(axis=0)

        for i in range(0, classes_x_times[category]):
            if strategy == "single":
                translation = translate_single(sent, languages[i], src)
                return_sentences = np.append(return_sentences, translation)
                return_all_classes.append(all_classes[idx])
            elif strategy == "double":
                translation = translate_double(sent, languages[i], src)
                return_sentences = np.append(return_sentences, translation)
                return_all_classes = np.append(return_all_classes, all_classes[idx])

    # write the data to a cache file
    write_cache_translation(file, (return_sentences, return_all_classes))
    return_all_classes = np.array(return_all_classes)
    return return_sentences, return_all_classes

