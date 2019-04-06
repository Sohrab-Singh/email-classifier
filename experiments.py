from model import *
from classifier import *


def baseline_experiment():
    parse_training_data()
    classify_test_data()


def word_length_filtering_experiment():
    parse_training_data(1)
    classify_test_data(1)
