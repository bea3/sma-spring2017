"""
Design a supervised machine learning classifier that will predict whether the impression of Facebook posts will be
greater than 1,000 based on data such as the type of post, weekday or weekend, and weather. Implement the classifier and
test it using Python. The data corpus contains data from Facebook on recent posts for a bicycle shop. The columns are
Post Message, Message Type, Date and Time of Post, Number of Impression, Weather indicator for snow or rain, and
weekday or weekend indicator for the post.

Test your classifier and calculate precision and recall. Turn in Python code for the classifier.
"""

import xlrd
import os
import DecisionTree
import csv
import sys
import numpy
from sklearn.ensemble import ExtraTreesRegressor
import random


"""
TODO
-get precision
"""
def csv_from_excel(excel_file):
    workbook = xlrd.open_workbook(excel_file)
    sheet = workbook.sheet_by_name('Key metrics')
    training_csv = open('training_data.csv', 'wb')
    testing_csv = open('test_data.csv', 'wb')
    training_writer = csv.writer(training_csv, quoting=csv.QUOTE_MINIMAL)
    testing_writer = csv.writer(testing_csv, quoting=csv.QUOTE_MINIMAL)

    header = ['', 'type', 'more_than_1000_impressions', 'weather', 'weekend']
    training_writer.writerow(header)

    training_id = 0
    testing_id = 0
    for x in xrange(1,sheet.nrows-1):
        row = sheet.row(x)
        row_values = []

        # parition data into 20% testing data, 80% training data
        random_number = random.randint(1, 100)
        if 1 <= random_number <= 10:
            testing_id += 1
            row_values.append(testing_id)
        else:
            training_id += 1
            row_values.append(training_id)

        for y in range(1, sheet.ncols):
            # skip date column
            if y == 2:
                continue

            # determine if number of impressions > 1000
            value = str(row[y].value)
            if y == 3:
                if row[y].value > 1000:
                    value = 1
                else:
                    value = 0

            if y == 5:
                print value
                if value == 'Y':
                    value = 1
                else:
                    value = 0

            # replace empty columns with "NA"
            if isinstance(value, basestring):
                if len(value) == 0:
                    value = "NA"
                else:
                    value = value.lower()

            row_values.append(value)

        if 1 <= random_number <= 30:
            testing_writer.writerow(row_values)
        else:
            training_writer.writerow(row_values)

    training_csv.close()
    testing_csv.close()


def decision_tree_classifier():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # get excel file
    files = os.listdir(os.curdir)
    excel_file = None

    for f in files:
        if ".xlsm" in f:
            excel_file = f
            break

    csv_from_excel(excel_file)

    dt = DecisionTree.DecisionTree(
                training_datafile='training_data.csv',
                csv_class_column_index=2,
                csv_columns_for_features=[1, 3, 4],
                entropy_threshold=0.01,
                max_depth_desired=8,
                symbolic_to_numeric_cardinality_threshold=10,
                csv_cleanup_needed=True)

    dt.get_training_data()
    dt.calculate_first_order_probabilities()
    dt.calculate_class_priors()
    dt.show_training_data()
    root_node = dt.construct_decision_tree_classifier()
    root_node.display_decision_tree("   ")

    tp = 0  # sum of true positives
    fp = 0  # sum of false positive
    fn = 0  # sum of false negatives
    tn = 0  # sum of true negatives

    print "\nClassifying with test data..."
    for line in open("test_data.csv"):
        csv_row = line.split(',')
        test_sample = ['type=' + csv_row[1],
                       'weather=' + csv_row[3],
                       'weekend=' + csv_row[4].replace('\r\n', '')]
        classification = dt.classify(root_node, test_sample)
        del classification['solution_path']
        which_classes = list(classification.keys())
        print("\nClassification with: " + str(test_sample) + "\n")
        print("     " + str.ljust("class name", 30) + "probability")
        print("     ----------                    -----------")
        more_than_1000 = 0
        less_than_1000 = 0
        for which_class in which_classes:
            if which_class is not 'solution_path':
                print("     " + str.ljust(which_class, 30) + str(classification[which_class]))
                if which_class == 'more_than_1000_impressions=1':
                    more_than_1000 = float(classification[which_class])
                elif which_class == 'more_than_1000_impressions=0':
                    less_than_1000 = float(classification[which_class])
        print "True Answer: " + csv_row[2]
        if more_than_1000 > less_than_1000 and csv_row[2] == '1':
            tp += 1
        elif more_than_1000 > less_than_1000 and csv_row[2] == '0':
            fp += 1
        elif more_than_1000 < less_than_1000 and csv_row[2] == '1':
            fn += 1
        elif more_than_1000 < less_than_1000 and csv_row[2] == '0':
            tn += 1

    if tp == 0 and fp == 0:
        print "\n\nPrecision = 0"
    else:
        print "\n\nPrecision = " + str(tp/(tp+fp))

    if tp == 0 and fn == 0:
        print "Recall = 0"
    else:
        print "Recall = " + str(tp/(tp+fn))


def extra_trees_regressor():
    etr = ExtraTreesRegressor(n_estimators=10, max_features=3, random_state=1)

def main():


if __name__ == "__main__": main()





