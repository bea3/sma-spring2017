import pandas
import numpy
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


#Note about data source: I used the first tab in the excel notebook and added a column called "output" using an if() command and it is a 1 if there are over 1000 impressions and a 0 otherwise

#import data set
bike_data = pandas.read_csv("./BikeFBImpressionData.csv")

#storing the column of interest as the target
target = "Output"

#filter to columns of interest
columns = bike_data.columns.tolist()
columns = [c for c in columns if c not in ["Type", "Weather", "Weekend"]]

#partition data into 80% training and 20% test
eighty = numpy.random.rand(len(bike_data)) < 0.8
train = bike_data[eighty]
test = bike_data[~eighty]


model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
print model

# Fitting the model to the training data
model.fit(train[columns], train[target])

# using the model on the test data
predictions = model.predict(test[columns])

# calculating the results
MSE = mean_squared_error(predictions, test[target])
print("MSE is " + MSE)