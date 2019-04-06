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


def smoothing_experiment():
    x = [round(i, 1) for i in np.linspace(0.1, 1, 11)]
    y = []
    print(x)
    for i in x:
        parse_training_data(ExperimentFilter.NONE)
        build_training_model(ExperimentFilter.NONE, i)
        y.append(classify_test_data(ExperimentFilter.NONE, i))
    print(y)
    plt.ylabel('Correct classification count')
    plt.xlabel('Smoothing factor')
    plt.title('Performance v/s Smoothing factor')
    plt.plot(x,y,'bo', color="red",linestyle="dotted")
    plt.savefig('PerformanceSmoothing.png')

