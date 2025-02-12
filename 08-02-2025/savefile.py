from scipy.io import savemat

# Save a dictionary to a MATLAB .mat file
data = {'arr': [1, 2, 3, 4, 5]}
savemat('output.mat', data)
