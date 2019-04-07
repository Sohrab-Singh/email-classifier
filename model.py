import os
import re
from experimentfilter import ExperimentFilter

ham_email_dictionary = {}
spam_email_dictionary = {}
ham_word_probability = {}
spam_word_probability = {}
ham_words_count = 0
spam_words_count = 0
ham_file_count = 0
spam_file_count = 0
probabilty_of_ham = 0
probabilty_of_spam = 0

vocabulary = set()


def parse_training_data(filter=ExperimentFilter.NONE):
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
            words = parse_filtered_words(words, filter)
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


def parse_stop_words_vocabulary():
    f = open(os.getcwd() + '/resources/English-Stop-Words.txt', "r", encoding='latin-1')
    stop_words_data = f.read().lower()
    stop_words = re.split('[^a-zA-Z]', stop_words_data)
    return stop_words


def parse_filtered_words(words, filter):
    if filter is ExperimentFilter.STOP_WORDS:
        stop_words = parse_stop_words_vocabulary()
        words = [x for x in words if x not in stop_words]
    elif filter is ExperimentFilter.WORD_LENGTH:
        words = [x for x in words if len(x) > 2 and len(x) < 9]
    
    return words


def sort_filter_word_count(word):
    return ham_email_dictionary.get(word, 0) + spam_email_dictionary.get(word, 0)


def filter_infrequent_words(filter, frequency):
    global vocabulary
    if filter is ExperimentFilter.INFREQUENT_WORDS_FREQUENCY_COUNT:
        if frequency == 1:
            vocabulary = [x for x in vocabulary if ham_email_dictionary.get(x, 0) + spam_email_dictionary.get(x, 0) != frequency]
        else:
            vocabulary = [x for x in vocabulary if ham_email_dictionary.get(x, 0) + spam_email_dictionary.get(x, 0) > frequency]
    elif filter is ExperimentFilter.INFREQUENT_WORDS_FREQUENCY_PERCENTAGE:
        vocabulary = sorted(vocabulary, key=sort_filter_word_count)
        n = int(frequency * len(vocabulary) / 100)
        del vocabulary[:n]
    vocabulary = set(vocabulary)
    return vocabulary


def find_smoothed_conditional_probabilities(word, delta):
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


def build_training_model(filter=ExperimentFilter.NONE, delta=0.5):
    if filter is ExperimentFilter.STOP_WORDS:
        f = open(os.getcwd() + '/resources/stopword-model.txt', 'w+')
    elif filter is ExperimentFilter.WORD_LENGTH:
        f = open(os.getcwd() + '/resources/wordlength-model.txt', 'w+')
    else:
        f = open(os.getcwd() + '/resources/baseline-model.txt', 'w+')
    line_count = 0
    for word in vocabulary:
        find_smoothed_conditional_probabilities(word, delta)
        line_count += 1
        f.write(get_model_word_info(line_count, word))
    f.close()





