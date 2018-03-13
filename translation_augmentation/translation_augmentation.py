from googletrans import Translator
from translation_augmentation.utilities import load_cache_translation, write_cache_translation
import os, sys
__name__ = translation_augmentation


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


def start ():
    print("module is running")
    print(determine_path())
    print("My various data files and so on are:")
    files = [f for f in os.listdir(determine_path() + "/things")]
    print(files)
    
if __name__ == "__main__":
    print("Decide what to do")


def augment_data(text, all_classes, classes_x_times, strategy="single", src="en"):
    '''
    This is a method that does text augmentation by translating the
    given text in another language and then translating it back in
    the original one. The text will have changed a bit
    (it will be different) but hopefully similar with the original
     text.
    :param src:
    :param text:
    :param all_classes:
    :param classes_x_times:
    :param strategy:
    :return:
    text            --> (X_train) the text we want to augment (and array of sentences)
    all_classes     --> (y_train) the classes that are present in each sentence
    classes_x_times --> dictionary containing the classes we want to augment
                        and how many times (up to 3 because we get good
                        translations only between the languages: English,Spanish,German,French)
    strategy        --> single : translate from the original language to another and back to the original
                                 e.g. EN to DE to EN
                        double : translate from the original language to 2 other languages and back to the original
                                 e.g. EN to DE to SP to EN
    src             --> in which language the initial text is in.Possible options 'en','de','sp','fr'

    '''

    translator = Translator()
    # in order to avoid this time consuming operation, cache the results
    file = os.getcwd()+"Translation/translation.p"
    try:
        print("Loading translation from cache.")
        cache = load_cache_translation(file)

        return cache
    except FileNotFoundError:
        print("Couldn't load translation from cache.")
        pass
    # X_train that will be returned
    return_sentences = []
    # y_train that will  be returned
    return_all_classes = []
    # all the available languages that we can make translations
    languages = ["en", "de", "fr", "sp"]
    languages.remove(src)

    def translate_single(text, dest):
        result1 = translator.translate(text, dest=dest, src=src)
        result2 = translator.translate(result1.text, dest=src, src=dest)
        return str(result2.text)

    def translate_double(text, dest):
        result1 = translator.translate(text, dest=dest, src="en")
        result2 = translator.translate(result1.text, dest='de', src=dest)
        result3 = translator.translate(result2.text, dest='en', src='de')
        return str(result3.text)

    for idx, sent in enumerate(text):
        print(idx, sent)
        sent = str(sent)
        return_sentences.append(text)
        return_all_classes.append(all_classes[idx])
        category = (all_classes[idx] == 1).argmax(axis=0)

        for i in range(1, classes_x_times[category]):
            if strategy == "single":
                translation = translate_single(sent, languages[i-1])
                return_sentences.append(translation)
                return_all_classes.append(all_classes[idx])
            else:
                translation = translate_double(sent, languages[i - 1])
                return_sentences.append(translation)
                return_all_classes.append(all_classes[idx])

    # write the data to a cache file
    write_cache_translation(file, (return_sentences, return_all_classes))

    return return_sentences, return_all_classes




