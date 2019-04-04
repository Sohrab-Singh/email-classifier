import os
import re

ham_email_dictionary = {}
spam_email_dictionary = {}
ham_word_probability = {}
spam_word_probability = {}
ham_words_count = 0
spam_words_count = 0
vocabulary = set()


def parse_training_data():
    path = os.getcwd() + '/resources/training data'
    global ham_words_count
    global spam_words_count
    for file in os.listdir(path):
        if file.endswith('.txt'):
            f = open(path + '/' + file, "r", encoding='latin-1')
            file_data_string = f.read().lower()
            words = re.split('[^a-zA-Z]', file_data_string)
            for word in words:
                if word is not '':
                    vocabulary.add(word)
                    if 'ham' in file:
                        if word in ham_email_dictionary:
                            ham_email_dictionary[word] = ham_email_dictionary[word] + 1
                        else:
                            ham_email_dictionary[word] = 1
                        ham_words_count += 1

                    if 'spam' in file:
                        if word in spam_email_dictionary:
                            spam_email_dictionary[word] = spam_email_dictionary[word] + 1
                        else:
                            spam_email_dictionary[word] = 1
                        spam_words_count += 1
            f.close()

    build_training_model()


def find_smoothed_conditional_probabilities(word, delta=0):
    ham_email_word_count = ham_email_dictionary[word] if word in ham_email_dictionary else 0
    spam_email_word_count = spam_email_dictionary[word] if word in spam_email_dictionary else 0
    ham_word_probability[word] = (ham_email_word_count + delta)/(ham_words_count * (1 + delta))
    spam_word_probability[word] = (spam_email_word_count + delta)/(spam_words_count * (1 + delta))


def get_model_word_info(line_count, word):
    return '{}  {}  {}  {}  {}  {}\n'.format(line_count, word, ham_email_dictionary.get(word, 0), ham_word_probability[word], spam_email_dictionary.get(word, 0), spam_word_probability[word])


def build_training_model():
    f = open(os.getcwd() + '/resources/model.txt', 'w+')
    line_count = 0
    for word in vocabulary:
        find_smoothed_conditional_probabilities(word)
        line_count += 1
        f.write(get_model_word_info(line_count, word))

    f.close()





