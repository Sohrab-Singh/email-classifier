from model import *
from classifier import *
from experimentfilter import ExperimentFilter
import numpy as np
import matplotlib.pyplot as plt


def baseline_experiment():
    parse_training_data()
    build_training_model()
    classify_test_data()


def stop_words_filtering_experiment():
    parse_training_data(ExperimentFilter.STOP_WORDS)
    build_training_model(ExperimentFilter.STOP_WORDS)
    classify_test_data(ExperimentFilter.STOP_WORDS)


def word_length_filtering_experiment():
    parse_training_data(ExperimentFilter.WORD_LENGTH)
    build_training_model(ExperimentFilter.WORD_LENGTH)
    classify_test_data(ExperimentFilter.WORD_LENGTH)


def classify_infrequent_word_filter_data(filter, frequency_value):
    parse_training_data()
    vocabulary = filter_infrequent_words(filter, frequency_value)
    x = len(vocabulary)
    build_training_model()
    y = classify_test_data()
    return x, y


def sort_tuple_list_key(tuple):
    return tuple[0]


def infrequent_word_filtering_experiment():
    x, y = [], []
    data = []
    x_val, y_val = classify_infrequent_word_filter_data(ExperimentFilter.INFREQUENT_WORDS_FREQUENCY_COUNT, 1)
    data.append((x_val, y_val))

    for i in range(5, 21, 5):
        x_val, y_val = classify_infrequent_word_filter_data(ExperimentFilter.INFREQUENT_WORDS_FREQUENCY_COUNT, i)
        data.append((x_val, y_val))
    
    for i in range(5, 26, 5):
        x_val, y_val = classify_infrequent_word_filter_data(ExperimentFilter.INFREQUENT_WORDS_FREQUENCY_PERCENTAGE, i)
        data.append((x_val, y_val))
    
    data.sort(key=sort_tuple_list_key)
    x = [tuple[0] for tuple in data]
    y = [tuple[1] for tuple in data]
    plt.ylabel('Correct classification count')
    plt.xlabel('No of words in vocabulary')
    plt.title('Performance against Words in Vocabulary')
    plt.plot(x, y, "bo", color="red", linestyle="dotted")
    plt.savefig('PerformanceInfrequentWords.png')
    

def smoothing_experiment():
    x = [round(i, 1) for i in np.linspace(0.1, 1, 11)]
    y = []
    for i in x:
        parse_training_data()
        build_training_model(ExperimentFilter.NONE, i)
        y.append(classify_test_data(ExperimentFilter.NONE, i))
    plt.ylabel('Correct classification count')
    plt.xlabel('Smoothing factor')
    plt.title('Performance against Smoothing factor')
    plt.plot(x,y,'bo', color="red",linestyle="dotted")
    plt.savefig('PerformanceSmoothing.png')

