import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import uuid

from s3_uploader import S3Uploader


class MatrixVisualizer():
    def __init__(self):
        self.s3_uploader = S3Uploader()

    def visualize_matrix(self, matrix, doc_names, labels):
        print('visualizing matrix...')

        unique_labels = list(set(labels))

        cmaps = ["Blues", "Greens", "Reds", "Purples", "Oranges", "Greys", "YlOrBr", "YlOrRd", "OrRd", "PuRd", "RdPu",
                 "BuPu", "GnBu", "PuBu", "YlGnBu", "PuBuGn", "BuGn", "YlGn"]
        fig, ax = plt.subplots()
        sns.set()
        for label in unique_labels:
            indices = [i for i, x in enumerate(labels) if x != label]
            self.heatmap_with_colors(matrix, doc_names, indices, cmaps[label])

        fig.set_size_inches(8, 8)
        fig.tight_layout()

        # generate random uuid
        id = uuid.uuid4()
        id = str(id) + ".png"
        self.create_image(plt, id)

        self.s3_uploader.upload_file(id)
        return self.s3_uploader.get_presigned_url(id)

    # create image from plot
    def create_image(self, plot, name):
        plot.savefig(name)
        plot.close()

    def heatmap_with_colors(self, sim_mat, cuisine_names, indices, cmap):
        sim_mat = self.set_cols_to_nan_as_copy(sim_mat, indices)
        sns.heatmap(sim_mat, vmin=0, vmax=1, xticklabels=cuisine_names, yticklabels=cuisine_names, cmap=cmap, cbar=False)

    def set_cols_to_nan_as_copy(self, matrix, indices):
        # create numpy array from matrix
        matrix_copy = np.array(matrix)
        # matrix_copy = matrix.copy()
        for i in indices:
            matrix_copy[:, i] = np.nan
        return matrix_copy

    # set size of plot
    def set_size(self):
        plt.figure(figsize=(width, height))