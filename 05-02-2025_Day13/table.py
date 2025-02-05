import matplotlib.pyplot as plt

data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
row_labels = ['Row 1', 'Row 2', 'Row 3']
col_labels = ['Col A', 'Col B', 'Col C']
# [x, y, width, height]
table = plt.table(data, loc='center',bbox=[0.1,0.4,0.5,0.2])
# plt.axis('off')
plt.show()