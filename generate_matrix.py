from scipy import spatial
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from matrix_visualizer import MatrixVisualizer


class MatrixClusterGenerator():
    def __init__(self):
        self.visualizer = MatrixVisualizer()

    def generate_matrix(self, json):
        print('generating matrix...')
        # get all the text

        print('loading text...')
        text = self.get_text(json)

        # get json keys as list of strings
        doc_names = list(json.keys())

        print(doc_names)
        # print(list())

        print('vectorizing...')

        # print(text)

        vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                                     min_df=2, stop_words='english',
                                     use_idf=True)
        # fit the vectorizer to the text
        X = vectorizer.fit_transform(text)

        kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=100, random_state=0)

        print('clustering...')
        kmeans.fit(X)

        labels = kmeans.labels_
        # sort labels in ascending order
        labels.sort()
        X = self.sort_X_by_label(X.toarray(), labels)
        doc_names = self.sort_doc_names_by_label(doc_names, labels)

        matrix = []
        for i, doc_a in enumerate(X):
            sim_vecs = []
            for j, doc_b in enumerate(X):
                if (i <= j):
                    w_sum = 1 - spatial.distance.cosine(doc_a, doc_b)
                else:
                    w_sum = matrix[j][i]
                sim_vecs.append(w_sum)

            matrix.append(sim_vecs)

        matrix = self.normalize_matrix(matrix)

        print('matrix created.')
        return self.visualizer.visualize_matrix(matrix, doc_names, labels)


    def normalize_matrix(self, matrix):
        for i, i_list in enumerate(matrix):
            my_max = max(i_list) + 0.000001
            for j, tt in enumerate(i_list):
                tt = tt / my_max
                matrix[i][j] = tt
        return matrix

    def sort_X_by_label(self, X, labels):
        X_with_label = [(X[i], labels[i]) for i in range(len(X))]
        X_with_label.sort(key=lambda x: x[1])
        return [x[0] for x in X_with_label]

    def sort_doc_names_by_label(self, doc_names, labels, should_print=False):
        doc_names_with_label = [(doc_names[i], labels[i]) for i in range(len(doc_names))]
        doc_names_with_label.sort(key=lambda x: x[1])
        if should_print:
            print(doc_names_with_label)
        return [x[0] for x in doc_names_with_label]

    def get_text(self, json):
        text = []
        # iterate over json keys
        for key in json.keys():
            text.append(str(json[key]))
        return text