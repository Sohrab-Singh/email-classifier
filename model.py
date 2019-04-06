import os
import re

ham_email_dictionary = {}
spam_email_dictionary = {}
ham_word_probability = {}
spam_word_probability = {}
ham_words_count = 0
spam_words_count = 0
ham_file_count = 0
spam_file_count = 0
probabilty_of_ham = 0.5
probabilty_of_spam = 0
delta = 0.5
vocabulary = set()


def parse_training_data():
    path = os.getcwd() + '/resources/training data'
    global ham_file_count
    global spam_file_count
    global ham_words_count
    global spam_words_count
    global probabilty_of_ham
    global probabilty_of_spam
    for file in os.listdir(path):
        if file.endswith('.txt'):
            if 'ham' in file:
                ham_file_count = ham_file_count + 1
            elif 'spam' in file:
                spam_file_count = spam_file_count + 1
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
                        ham_words_count = ham_words_count + 1

                    if 'spam' in file:
                        if word in spam_email_dictionary:
                            spam_email_dictionary[word] = spam_email_dictionary[word] + 1
                        else:
                            spam_email_dictionary[word] = 1
                        spam_words_count = spam_words_count + 1
            f.close()
    probabilty_of_ham = ham_file_count/(ham_file_count + spam_file_count)
    probabilty_of_spam = spam_file_count/(ham_file_count + spam_file_count)
    build_training_model()


def find_smoothed_conditional_probabilities(word):
    ham_email_word_count = ham_email_dictionary[word] if word in ham_email_dictionary else 0
    spam_email_word_count = spam_email_dictionary[word] if word in spam_email_dictionary else 0
    ham_word_probability[word] = (ham_email_word_count + delta)/(ham_words_count * (1 + delta))
    spam_word_probability[word] = (spam_email_word_count + delta)/(spam_words_count * (1 + delta))


def get_model_word_info(line_count, word):
    return '{}  {}  {}  {}  {}  {}\n'.format(line_count, word, ham_email_dictionary.get(word, 0), ham_word_probability[word], spam_email_dictionary.get(word, 0), spam_word_probability[word])


def get_ham_probability():
    return probabilty_of_ham


def get_spam_probability():
    return probabilty_of_spam


def get_ham_words_count():
    return ham_words_count


def get_spam_words_count():
    return spam_words_count


def build_training_model():
    f = open(os.getcwd() + '/resources/model.txt', 'w+')
    line_count = 0
    for word in vocabulary:
        find_smoothed_conditional_probabilities(word)
        line_count += 1
        f.write(get_model_word_info(line_count, word))

    f.close()





