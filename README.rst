# Text_Augmentation_via_Translation
A simple method to augment text by using NMT (neural machine translation).

!! Note!! If you have any issues using this library or you feel that it is lacking something don't hesitate to message me.

How to use (Linux Dist.):

1.Install using pip ---> pip install translation-augmentation

2.Import the library---> from translation_augmentation.translation_augmentation import augment_data_simple
                         from translation_augmentation.translation_augmentation import augment_data



Example:

1.
from translation_augmentation.translation_augmentation import augment_data_simple
import numpy as np

s1 = "The food was awful"
s2 = "That was the best meal I have had in ages."
# the sentences we want to augment 
X_train = np.array([s1, s2])
# how many times we want to augment each sentence
times = 2
X_train_new = augment_data_simple(X_train, times)
print("Original: ", X_train)
print("After augmentation: ", X_train_new)

>>Original:  ['The food was awful' 'That was the best meal I have had in ages.']

>>After augmentation:  ['The food was awful'
                        'The food was terrible'
                        'The food was horrible'
                        'That was the best meal I have had in ages.'
                        'This was the best meal I have had in years.'
                        'It was the best meal I had in a long time.']



2.
from translation_augmentation.translation_augmentation import augment_data
import numpy as np

s1 = "The food was awful"
s2 = "That was the best meal I have had in ages."
# the sentences we want to augment
X_train = np.array([s1, s2])
# the class that is present in each sentense in binary(in this case we have sentiment for each sentece either positive,negative or neutral)
y_train = np.array([[0, 1, 0], [1, 0, 0]])
# how many times we want to augment each class (dictionary stating)
classes_x_times = {}
classes_x_times[0] = 1 # double the first class
classes_x_times[1] = 2 # trible the second class
classes_x_times[2] = 0 # leave the trird class as it is

X_train_new, y_train_new = augment_data(X_train, y_train, classes_x_times)
print("Original: ", X_train, "\n", y_train)
print("After augmentation: ", X_train_new, "\n", y_train_new)

>>Original:  ['The food was awful' 'That was the best meal I have had in ages.'] 
 [[0 1 0]
 [1 0 0]]

>>After augmentation:  ['The food was awful' 
                       'The food was terrible' 
                       'The food was horrible'
                       'That was the best meal I have had in ages.'
                       'This was the best meal I have had in years.'] 
 [[0, 1, 0],
  [0, 1, 0], 
  [0, 1, 0],
  [1, 0, 0],
  [1, 0, 0]]



Method Documentations:
1.
### augment_data_simple ###
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
    times           --> how many times we want to augment each given sentence (up to 3 because
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

2.
### augment_data ###
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


