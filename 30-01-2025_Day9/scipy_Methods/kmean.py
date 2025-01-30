import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import whiten, vq, kmeans, kmeans2

def whiten_data(arr):
    # Whiten the data (scale features to unit variance).
    return whiten(arr)

def find_codebook(features, code_book):
    # Assign features to the nearest centroids from the codebook using vector quantization.
    return vq(features, code_book)

def perform_kmeans_on_data(features, num_clusters):
    # Perform k-means clustering on the given features and return the centroids.
    # Whiten the features before performing k-means
    whitened = whiten_data(features)
    codebook, distortion = kmeans(whitened, num_clusters)
    return codebook, distortion

def plot_clusters_with_centroids(features, codebook):
    
    # Plot the clustered data and their centroids.
    plt.scatter(features[:, 0], features[:, 1])
    plt.scatter(codebook[:, 0], codebook[:, 1], c='r', label='Centroids')
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend()
    plt.show()

def kmeans_with_initial_centroids(features, num_clusters, initial_centroids):
    
    # Perform k-means clustering with specified initial centroids.
    whitened = whiten_data(features)
    centroid, label = kmeans2(whitened, num_clusters, minit=initial_centroids)
    return centroid, label

def plot_kmeans_clusters(features, label, centroid):
    
    # Plot the results of k-means clustering with labeled points and centroids.
    w0 = features[label == 0]
    w1 = features[label == 1]
    w2 = features[label == 2]

    plt.plot(w0[:, 0], w0[:, 1], 'o', alpha=0.5, label='Cluster 0')
    plt.plot(w1[:, 0], w1[:, 1], 'd', alpha=0.5, label='Cluster 1')
    plt.plot(w2[:, 0], w2[:, 1], 's', alpha=0.5, label='Cluster 2')
    plt.plot(centroid[:, 0], centroid[:, 1], 'k*', label='Centroids')
    plt.axis('equal')
    plt.legend(shadow=True)
    plt.show()

# Example 1: Using whiten and vq (vector quantization) for simple data
def example_1():
    arr = np.array([[1, 2, 3, 4],
                    [5, 6, 7, 8],
                    [9, 10, 11, 12]])

    print("Whitened Data (Example 1):")
    print(whiten_data(arr))

    code_book = np.array([[1., 1., 1.],
                          [2., 2., 2.]])
    features = np.array([[1.9, 2.3, 1.7],
                         [1.5, 2.5, 2.2],
                         [0.8, 0.6, 1.7]])

    print("vq Result (Example 1):")
    print(find_codebook(features, code_book))

# Example 2: Performing k-means clustering
def example_2():
    features = np.array([[1, 2],
                         [3, 4],
                         [10, 25],
                         [50, 100],
                         [5, 7]])

    print("Whitened Features (Example 2):")
    print(whiten_data(features))

    # Set initial centroids based on the whitened data
    centroid = np.array((features[0], features[2]))
    print("Initial Centroids (Example 2):")
    print(centroid)

    print("k-means Result (Example 2):")
    codebook, distortion = perform_kmeans_on_data(features, 3)
    print(f"Codebook (Centroids):\n{codebook}")
    print(f"Distortion: {distortion}")

    # Plot the results
    plot_clusters_with_centroids(features, codebook)

# Example 3: Generating synthetic data and applying k-means clustering
def example_3():
    pts = 50
    rng = np.random.default_rng()
    # Generate two clusters of data
    a = rng.multivariate_normal([0, 0], [[4, 1], [1, 4]], size=pts)
    b = rng.multivariate_normal([30, 10], [[10, 2], [2, 1]], size=pts)
    features = np.concatenate((a, b))

    # Whiten the data before clustering
    whitened = whiten_data(features)

    # Apply k-means clustering to find 2 clusters
    codebook, distortion = kmeans(whitened, 3)

    # Plot the whitened data and centroids
    plot_clusters_with_centroids(features, codebook)

# Example 4: K-means with initial centroids using kmeans2
def example_4():
    rng = np.random.default_rng()
    a = rng.multivariate_normal([0, 6], [[2, 1], [1, 1.5]], size=45)
    b = rng.multivariate_normal([2, 0], [[1, -1], [-1, 3]], size=30)
    c = rng.multivariate_normal([6, 4], [[5, 0], [0, 1.2]], size=25)
    features = np.concatenate((a, b, c))

    # Shuffle the data
    rng.shuffle(features)

    # Apply k-means with initial centroids
    centroid, label = kmeans_with_initial_centroids(features, 3, 'points')

    # Print the cluster counts
    counts = np.bincount(label)
    print(f"Cluster Counts (Example 4): {counts}")

    # Plot the results of k-means clustering
    plot_kmeans_clusters(features, label, centroid)

# Run the examples
example_1()
example_2()
example_3()
example_4()
