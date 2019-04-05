from model import *
from math import log10


def classify_email(file_path):
    ham_score = log10(probabilty_of_ham)
    spam_score = log10(probabilty_of_spam)
    f = open(file_path, "r", encoding='latin-1')
    file_data_string = f.read().lower()
    words = re.split('[^a-zA-Z]', file_data_string)
    for word in words:
        if word is not '':
            ham_score = ham_score*log10(ham_word_probability[word])
            spam_score = spam_score*log10(spam_word_probability[word])

    f.close()
    return 'ham' if ham_score > spam_score else 'spam', ham_score, spam_score


def classify_test_data():
    path = os.getcwd() + '/resources/test data'
    f = open(os.getcwd() + '/resources/baseline-result.txt', 'w+')
    line_counter = 0
    for file in os.listdir(path):
        if file.endswith('.txt'):
            line_counter = line_counter + 1
            file_category = 'ham' if 'ham' in file else 'spam'
            email_category, ham_score, spam_score = classify_email(path + '/' + file)
            result = 'right' if file_category == email_category else 'wrong'
            f.write('{}  {}  {}  {}  {}  {}  {}\n'.format(line_counter, file, email_category, ham_score, spam_score, file_category,result))

    f.close()


