from model import *


def classify_email(file_path):
    ham_score = probabilty_of_ham
    spam_score = probabilty_of_spam
    f = open(file_path, "r", encoding='latin-1')
    file_data_string = f.read().lower()
    words = re.split('[^a-zA-Z]', file_data_string)
    for word in words:
        if word is not '':
            ham_score = ham_score*ham_word_probability[word]
            spam_score = spam_score*spam_word_probability[word]

    f.close()
    return 'ham' if ham_score > spam_score else 'spam'