from scipy import ndimage
input =  [0,1,2,3]
labels = [1,1,2,2]
a=ndimage.sum_labels(input, labels, index=[1,2])
b=ndimage.sum_labels(input, labels, index=1)
c=ndimage.sum_labels(input, labels)
print(a)
print(b)
print(c)