import os
import re

ham_email_dictionary = {}
spam_email_dictionary = {}


def parse_training_data():
    path = os.getcwd() + '/resources/training data'
    for file in os.listdir(path):
        if file.endswith('.txt'):
            f = open(path + '/' + file, "r", encoding='latin-1')
            file_data_string = f.read().lower()
            words = re.split('[^a-zA-Z]',file_data_string)
            for word in words:
                if word is not '':
                    if 'ham' in file:
                        if word in ham_email_dictionary:
                            ham_email_dictionary[word] = ham_email_dictionary[word] + 1
                        else:
                            ham_email_dictionary[word] = 1

                    if 'spam' in file:
                        if word in spam_email_dictionary:
                            spam_email_dictionary[word] = spam_email_dictionary[word] + 1
                        else:
                            spam_email_dictionary[word] = 1

    print(ham_email_dictionary)
    print(spam_email_dictionary)











