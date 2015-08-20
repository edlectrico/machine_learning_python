import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

# digits contains images, data, target...
# http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html
digits = datasets.load_digits()
# print digits.data.shape	# (1797, 64) 1797 examples of digit data in 8x8 matrices
# print len(digits.data)	# 1797

# Visualizing some sample data
'''
plt.gray()
plt.matshow(digits.images[0]) # prints the first image (obviously, its zero)
print digits.data[0]
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

data = digits.data[:-1] # from 1797 we pick all but the last element to train, the last one to test
target = digits.target[:-1]
'''
data = digits.data[:-10]
target = digits.target[:-10]
'''

'''
print data
print target
'''
# Training the classifier
classifier.fit(data, target)

# Predicting the 1st from the last element (the negative first element)
print 'Prediction: ' + str(classifier.predict(digits.data[-1]))
'''
print 'Prediction: ' + str(classifier.predict(digits.data[-2]))
'''

# Visualization with matplotlib
plt.imshow(digits.images[-1], cmap=plt.cm.gray_r, interpolation='nearest')
'''
plt.imshow(digits.images[-2], cmap=plt.cm.gray_r, interpolation='nearest')
'''
plt.show()
