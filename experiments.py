from model import *
from classifier import *
import numpy as np
import matplotlib.pyplot as plt


def baseline_experiment():
    parse_training_data()
    classify_test_data()


def word_length_filtering_experiment():
    parse_training_data(1)
    classify_test_data(1)


def smoothing_experiment():
    x = [round(i,1) for i in np.linspace(0.1,1,11)]
    y = []
    print(x)
    for i in x:
        parse_training_data(0,i)
        y.append(classify_test_data(0,i))
    print(y)
    plt.ylabel('Correct classification count')
    plt.xlabel('Smoothing factor')
    plt.title('Performance v/s Smoothing factor')
    plt.plot(x,y,'bo', color="red",linestyle="dotted")
    plt.savefig('PerformanceSmoothing.png')

