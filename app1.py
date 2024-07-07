import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import pandas as pd

# Define the points S1 to S6 with their x and y coordinates
points = {
    'S1': (1, 2),
    'S2': (3, 4),
    'S3': (5, 6),
    'S4': (7, 8),
    'S5': (9, 10),
    'S6': (11, 12)
}


# Function to calculate Euclidean distance between two points
def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Function to generate the adjacency matrix
def generate_adjacency_matrix(points):
    num_points = len(points)
    adjacency_matrix = np.zeros((num_points, num_points))

    for i, (key1, point1) in enumerate(points.items()):
        for j, (key2, point2) in enumerate(points.items()):
            if i != j:
                distance = euclidean_distance(point1, point2)
                adjacency_matrix[i, j] = distance

    return adjacency_matrix


# Perform hierarchical clustering
adjacency_matrix = generate_adjacency_matrix(points)
Z = linkage(adjacency_matrix, method='single')

# Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(Z, labels=list(points.keys()), orientation='top', distance_sort='descending')
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Data Points')
plt.ylabel('Distance')
plt.show()

# Assign clusters using a distance threshold
threshold = 4  # Adjust this threshold as needed
clusters = fcluster(Z, threshold, criterion='distance')

# Visualize clusters
for cluster_num in np.unique(clusters):
    cluster_points = np.array([points[key] for key, cluster in zip(points.keys(), clusters) if cluster == cluster_num])
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster_num}')

plt.title('Cluster Visualization')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

# Export cluster results to CSV
data = {
    'Point': list(points.keys()),
    'Cluster': clusters
}
df = pd.DataFrame(data)
df.to_csv('cluster_results.csv', index=False)

print("Cluster results exported to 'cluster_results.csv'.")
