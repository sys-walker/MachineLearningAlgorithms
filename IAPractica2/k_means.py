import random as r
import matplotlib.pyplot as plt
import numpy as np
from treepredict import read_file

class Kmeans:
    def __init__(self,k,distance,max_iters,use_range=True,verbose=False):
        self.k=k
        self.distance = distance
        self.use_range= use_range
        self.max_iters = max_iters
        self.verbose_mode=verbose
        # use_range : select random value in the range(True) or select ponts as centroids...
        self.centroids=list()
    def _get_range_random_value(self,points,feature_idx):
        """
        Get a random value inside the feature range. The values
        where this range is extracted for are the ones present
        in the points data.
        """
        feat_values=[point[feature_idx] for point in points]
        feat_max = max(feat_values)
        feat_min =  min(feat_values)
        return r.random()*(feat_max-feat_min)+feat_min
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
        self.centroids=[]
        while True:
            if len(self.centroids) == self.k:
                break
            generated_idx = r.randint(0, len(points) - 1)
            centroid = points[generated_idx]
            if centroid not in self.centroids:
                self.centroids.append(centroid)
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
        """
        #1. Set the k centroids randomly
        if self.use_range:
            self._create_random_centroids(rows)
            if self.verbose_mode:
                print("Generated centroids from X,Y\n",self.centroids,"\n")
        else:
            self._create_points_centroids(rows)
            if self.verbose_mode:
                print("Created centroids from given data\n", self.centroids,"\n")


        lastmatches=None
        for iteration in range(self.max_iters):
            if self.verbose_mode:
                print("Iteration ",iteration)
            bestmatches = [[] for k in range(self.k)]
            for  row_idx,row in enumerate(rows):
                centroid = self._get_closest_centroid(row)
                bestmatches[centroid].append(row_idx)
            if self.verbose_mode:
                print("\tAssignation:",bestmatches)

            # end/stop/goal condition
            if bestmatches==lastmatches:
                if self.verbose_mode:
                    print("The centroids did not change. Stopped Algorithm")
                break

            lastmatches = bestmatches
            self._update_centroids(bestmatches,rows)
        self.inertia_ = self._calculateInertia(lastmatches,rows)
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
    def _calculateInertia(self, data_indexes,rows):
        d =[]
        i=0
        for c in self.centroids:
            d.append(self._intracentroid_distance(c,data_indexes[i],rows))
            i+=1

        return sum(d)
    def _intracentroid_distance(self, centroid,indexes_assigned,rows):
        i_result=float(0)
        #print("centroide =",centroid,"--",[rows[j] for j in indexes_assigned])
        for j in indexes_assigned:
            i_result+=self.distance(rows[j],centroid)
        return i_result



def euclidean_squared(p1, p2):
    return sum(
        (p1 - p2) ** 2
        for p1, p2 in zip(p1, p2)
    )






def total_distance_function(rows, K_inicial=2, K_final=10,use_range=False,verbose_mode=False):
    inertias=[]
    print("Inertias between Clusters K0=",K_inicial,", K=",K_final)
    print("K\tInertia")
    rangeK=range(K_inicial,K_final+1)
    for k in rangeK:
        kmeans_test = Kmeans(k=k,distance=euclidean_squared,use_range=use_range,max_iters=100,verbose=verbose_mode)
        kmeans_test.fit(rows)
        print (k,"\t",kmeans_test.inertia_)
        inertias.append(kmeans_test.inertia_)
    plt.plot(rangeK,inertias, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method using Inertia')
    plt.show()


if __name__ == '__main__':
    #data = [(1, 1),(2, 1),(4, 3),(5, 4),]
    data = read_file("seeds.csv",",")
    total_distance_function(data,K_inicial=2,K_final=8)


    # dataset = seeds.csv
    #kmeans = Kmeans(k=6, distance=euclidean_squared,use_range=True, max_iters=1000,verbose=True)
    #bestmatches = kmeans.fit(data)
    # print("\nResult")
    # print("data=",data)
    # print("bestmatches", bestmatches)
    # print("Centroids: ", kmeans.centroids)
    # print("Predictions", kmeans.predict(data))
    # print("inertia = ",kmeans.inertia_)

