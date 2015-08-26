import numpy as np
import matplotlib.pyplot as pl
from sklearn import svm

# We have coordinate pairs that are "low" numbers and pairs that are "higher" numbers.
# We assign 0 to the lower coordinate pairs and 1 to the higher feature pairs.
X = np.array([[1,2],
             [5,8],
             [1.5,1.8],
             [8,8],
             [1,0.6],
             [9,11]])

y = [0,1,0,1,0,1]	# labels (targets)

clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)

print clf.predict([0.58,0.76])		# It predicts a 0 since is a "lower" coordinate pair
# print clf.predict([10.58,10.76])	# It predicts a 1

# Visualization
w = clf.coef_[0]
print w

a = -w[0] / w[1]

xx = np.linspace(0,12)
yy = a * xx - clf.intercept_[0] / w[1]

h0 = pl.plot(xx, yy, 'k-', label="non weighted div")

pl.scatter(X[:, 0], X[:, 1], c = y)
pl.legend()

# pl.scatter(x, y)
pl.show()
