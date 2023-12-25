import pandas as pd
from sklearn.neighbors import NearestNeighbors

class MyModel:
    def __init__(self, df_path: str) -> None:
        # Здесь может быть долгая загрузка модели model_path
        self.df = pd.read_csv('../data/with_clusters.csv')
        
        
    def search(self, product_id: str) -> list:
        product = df[df['product_id'] == product_id]
        cluster_id = product['cluster'].values[0]
        product = product.drop(columns = ['product_id', 'cluster'])
        cluster = df[df['cluster'] == cluster_id]
        cluster = cluster.reset_index(drop=True)
        knn = NearestNeighbors(n_neighbors=n)
        knn.fit(cluster.drop(columns = ['product_id', 'cluster']))
        neighbors = knn.kneighbors(product, 5, return_distance=False)
        answer = []
        for i in neighbors[0]:
            answer.append(cluster.loc[i])
        return pd.DataFrame(columns=cluster.columns.to_list(), data=answer)