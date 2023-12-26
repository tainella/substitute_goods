import pandas as pd
from sklearn.neighbors import NearestNeighbors

class MyModel:
    """Класс модели,осуществлающий поиск товара заменителя.
    """
    def __init__(self, df_path: str = '../data/with_clusters.csv', n: int = 5) -> None:
        self.df = pd.read_csv(df_path)
        self.n = n
        

    def search(self, product_id: str) -> list:
        product = self.df[self.df['product_id'] == product_id]
        cluster_id = product['cluster'].values[0]
        product = product.drop(columns = ['product_id', 'cluster'])
        cluster = self.df[self.df['cluster'] == cluster_id]
        cluster = cluster.reset_index(drop=True)
        knn = NearestNeighbors(n_neighbors=self.n)
        knn.fit(cluster.drop(columns = ['product_id', 'cluster']))
        neighbors = knn.kneighbors(product, 5, return_distance=False)
        answer = []
        for i in neighbors[0]:
            answer.append(cluster.loc[i]['product_id'])
        return answer