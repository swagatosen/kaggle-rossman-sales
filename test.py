import sklearn
import swagML as sml
import numpy as np
import matplotlib.pyplot as plt

# testArr = [1, 1, 1, 1, 5, 6, 7, 8, 9, 10]
# shuffled = sklearn.utils.shuffle(testArr)

# print(testArr)
# print(shuffled)

# for i in range(5):
# 	x = np.array(range(10))
# 	y1 = np.random.rand(10)
# 	y2 = np.random.rand(10)

# 	plt.subplot(1, 5, i + 1)
# 	plt.plot(x, y1, label='y1 i = ' + str(i))
# 	plt.plot(x, y2, label='y2 i = ' + str(i))
# 	plt.legend()
# 	# plt.plot(x, y1, label='y1')
# 	# plt.plot(x, y2, label='y2')


# plt.show()

actuals = np.array([1, 0, 0, 2])
pred = np.array([1, 1, 1, 1])

mean1 = sml.EvaluateOutput_Deviation(actuals, pred)
print("mean1: {0}".format(mean1) )