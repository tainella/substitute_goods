class MyModel:
    def __init__(self, model_path: str, df_path: str) -> None:
        # Здесь может быть долгая загрузка модели model_path
        self.model = None 
        self.df = None
        
        
    def make_prediction(self, search_text: str) -> list:
        return ['Картошечка', 'Баклажанчики', 'Яички', 'Кура', 'Пицца из трешки']
    
    def search(self, text: str) -> dict:
        pass