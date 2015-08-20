import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

# digits contains images, data, target...
# http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html
digits = datasets.load_digits()
# print digits.data.shape	# (1797, 64)

# Visualizing some sample data
'''
plt.gray()
plt.matshow(digits.images[0]) # prints the first image (obviously, its zero)
plt.show()
'''
'''
print digits.data	# current available data (features)
print digits.target	# the label we assign to the digits
			# 'target_names': array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
'''
# Creating the classifier 
# http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
classifier = svm.SVC(gamma=0.001) # The gamma parameter is optional

data = digits.data[:-10] 	# all but the last 10 to train, the last 10 to test
target = digits.target[:-10]
'''
print data
print target
'''
# Training the classifier
classifier.fit(data, target)

# Predicting the 5th from the last element
print 'Prediction: ' + str(classifier.predict(digits.data[-5]))

# Visualization with matplotlib
plt.imshow(digits.images[-5], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()
