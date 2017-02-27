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
from post_model import Post
import DecisionTree
import csv
import sys

decision_trees = []

# def set_training_data(excel_file):
#     workbook = xlrd.open_workbook(excel_file)
#
#     sheet = workbook.sheet_by_name("Key metrics")
#
#     for x in range(1, sheet.nrows):
#         row = sheet.row(x)
#
#         is_weekend = None
#         if row[5].value == "Y":
#             is_weekend = True
#         else:
#             is_weekend = False
#
#         new_post = Post(row[1].value.encode("UTF-8"), is_weekend, row[4].value.encode("UTF-8"))
#
#         # find if combination is already in the set
#         has_post = False
#         for y in range(len(decision_trees)):
#             if decision_trees[y].equals(new_post):
#                 has_post = y
#                 break
#
#         # if combination is not in the list, add it
#         if has_post == False:
#             new_post.append_impression(row[3].value)
#             decision_trees.append(new_post)
#         # if it is, add the new impression number
#         else:
#             decision_trees[has_post].append_impression(row[3].value)
#
# def main():
#     # get excel file
#     files = os.listdir(os.curdir)
#     excel_file = None
#
#     for f in files:
#         if ".xlsm" in f:
#             excel_file = f
#             break
#
#     set_training_data(excel_file)
#
#     workbook = xlrd.open_workbook(excel_file)
#     for x in range(1, workbook.nsheets):
#         sheet = workbook.sheet_by_index(x)
#         print sheet.name

def csv_from_excel(excel_file):
    workbook = xlrd.open_workbook(excel_file)
    sheet = workbook.sheet_by_name('Key metrics')
    csv_file = open('training_data.csv', 'wb')
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for x in xrange(1,sheet.nrows):
        row = sheet.row(x)
        row_values = []
        row_values.append(x)
        for y in range(1, sheet.ncols):
            if y == 2:
                continue
            value = str(row[y].value)
            if y == 3:
                if row[y].value > 1000:
                    value = True
                else:
                    value = False
            row_values.append(value)
        writer.writerow(row_values)

    csv_file.close()

def main():
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
                training_datafile = 'training_data.csv',
                csv_class_column_index = 2,
                csv_columns_for_features = [1,3,4],
                entropy_threshold = 0.01,
                max_depth_desired = 8)

    dt.get_training_data()
    dt.calculate_first_order_probabilities()
    dt.calculate_class_priors()
    dt.show_training_data()
    root_node = dt.construct_decision_tree_classifier()
    root_node.display_decision_tree("   ")



if __name__ == "__main__": main()





