import random
class Kmeans:
    def __init__(self,k,distance,max_iters,use_range=True):
        self.k=k
        self.distance = distance
        self.use_range= use_range
        self.max_iters = max_iters
        # use_range : select random value in the range(True) or select ponts as centroids...
        self.centroids=list()
    def _get_range_random_value(self,points,feature_idx):
        """
        Get a random value inside the feature range. The values
        where this range is extracted for are the ones present
        in the points data.

        :param points:
        :param feature_idx:
        :return:
        """
        feat_values=[point[feature_idx] for point in points]
        feat_max = max(feat_values)
        feat_min =  min(feat_values)
        return random.random()*(feat_max-feat_min)+feat_min
    def _create_random_centroids(self,points):
        """Random centroids in the range of the points"""
        n_feats = len(points[0])
        for cluster_idx in range(self.k):
            point = [0.0] *n_feats
            for feature_idx in range(n_feats):
                point[feature_idx] = self._get_range_random_value(points,feature_idx)
            self.centroids.append(point)
    def _create_points_centroids(self,points):
        """Random points selected as centrodis"""
        raise NotImplementedError
    def _get_closest_centroid(self, row):
        """

        :param row: point -> calculate distance
        :return:
        """
        min_dist=2**64
        closest = None
        for centroid_idx, centroid in enumerate(self.centroids):
            dist =  self.distance(row,centroid)
            if dist < min_dist:
                min_dist = dist
                closest = centroid_idx
        return closest
    def _average_points(self,points):
        n_points = len(points)
        n_feats = len(points[0])
        avrg = [0.0] *n_feats
        # (1,2),(2,3),(44,2)
        for feat in range(n_feats):
            feat_values = [point[feat] for point in points]
            avrg[feat] =sum(feat_values)/ n_points
        return avrg
    def _update_centroids(self, bestmatches,rows):
        # bestmatches = [[1,2,3],[4,5],[6]]
        for centroid_idx in range(self.k):
            points =[rows[point_idx]for point_idx in bestmatches[centroid_idx]]
            if not points:
                continue
            avrg=self._average_points(points)
            self.centroids[centroid_idx] = avrg
    def fit(self,rows):
        """
        Fit the model
        :param rows:
        :return:
        """
        #1. Set the k centroids randomly
        if self.use_range:
            self._create_random_centroids(rows)
        else:
            self._create_points_centroids(rows)

        lastmatches=None
        for iteration in range(self.max_iters):
            print("Iteration ",iteration)
            bestmatches = [[] for k in range(self.k)]
            for  row_idx,row in enumerate(rows):
                centroid = self._get_closest_centroid(row)
                bestmatches[centroid].append(row_idx)
            print("\tAssignation:",bestmatches)

            # end/stop/goal condition
            if bestmatches==lastmatches:
                print("The centroids did not change. Stopped Algorithm")
                break

            lastmatches = bestmatches
            self._update_centroids(bestmatches,rows)
        return lastmatches

    def predict(self,rows):
        """
        Predict the closest cluster each sample in rows belong to.
        what does map(self._get_closest_centroid,rows)

        result=[]
        for row in rows:
            result.append(self._get_closest_centroid(row))
        return result



        :param rows: points
        :return:
        """
        return list(map(self._get_closest_centroid,rows))


def euclidean_squared(p1, p2):
    return sum(
        (p1 - p2) ** 2
        for p1, p2 in zip(p1, p2)
    )




if __name__ == '__main__':
    data = [
        (1, 1),
        (2, 1),
        (4, 3),
        (5, 4),
    ]
    kmeans = Kmeans(k=2, distance=euclidean_squared, max_iters=5)
    bestmatches = kmeans.fit(data)
    print("\nResult")
    print("bestmatches", bestmatches)
    print("Centroids: ", kmeans.centroids)
    print("Predictions", kmeans.predict(data))

