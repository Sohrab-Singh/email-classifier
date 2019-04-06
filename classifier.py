from model import *
from math import log10


def classify_email(file_path, delta):
	ham_score = log10(get_ham_probability())
	spam_score = log10(get_spam_probability())
	f = open(file_path, "r", encoding='latin-1')
	file_data_string = f.read().lower()
	words = re.split('[^a-zA-Z]', file_data_string)
	for word in words:
		if word is not '':
			ham_score = ham_score + log10(ham_word_probability.get(word, delta/(get_ham_words_count() * (1 + delta))))
			spam_score = spam_score + log10(spam_word_probability.get(word, delta/(get_spam_probability() * (1 + delta))))

	f.close()
	return 'ham' if ham_score > spam_score else 'spam', ham_score, spam_score


def classify_test_data(is_word_filtering=0,delta=0.5):
	path = os.getcwd() + '/resources/test data'
	if is_word_filtering:
		f = open(os.getcwd() + '/resources/wordlength-result.txt', 'w+')
	else:
		f = open(os.getcwd() + '/resources/baseline-result.txt', 'w+')
	line_counter = 0
	correct_result_counter = 0
	for file in os.listdir(path):
		if file.endswith('.txt'):
			line_counter = line_counter + 1
			file_category = 'ham' if 'ham' in file else 'spam'
			email_category, ham_score, spam_score = classify_email(path + '/' + file,delta)
			result = 'right' if file_category == email_category else 'wrong'
			correct_result_counter = (correct_result_counter + 1) if result is 'right' else correct_result_counter
			f.write('{}  {}  {}  {}  {}  {}  {}\n'.format(line_counter, file, email_category, ham_score, spam_score, file_category,result))

	f.close()
	return correct_result_counter


