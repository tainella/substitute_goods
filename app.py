import pandas as pd
import streamlit as st

from model.model import MyModel

@st.cache_resource()
def load_model(df_path: str = 'path/to/df') -> MyModel:
    """Логика загрузки модели машинного обучения.

    Args:
        df_path (str, optional): Путь до датафрейма в котором будет производится поиск. Defaults to 'path/to/df'.

    Returns:
        MyModel: Загруженная модель.
    """
    return MyModel(model_path, df_path)

def load_df(df_path: str = 'data/worked_data.csv') -> pd.DataFrame:
    """Логика загрузки датафрейма в страницу.

    Args:
        df_path (str, optional): Путь до базового датафрейма. Defaults to 'data/worked_data.csv'.

    Returns:
        pd.DataFrame: Предобработанный датафрейм.
    """
    df = pd.read_csv(df_path)
    df = df.drop(columns = ['Unnamed: 0', 'product_id'])
    return df


def main():
    # Sidebar Search
    form = st.sidebar.form(key='Search')
    form.header("Поисковый запрос")

    search_text = form.text_input('Введите название товара:')
    form.form_submit_button('Поиск')

    # Sidebar Contributors

    with st.sidebar.expander('Команда разработки'):
        st.image('data/team.jpg')
        st.markdown('''
                    1. Амелия Полей-Добронравова: `dev`, `ml`, `tamlead`
                    2. Кира Лейченко: `dev`, `ml`
                    3. Мария Кондаратцева: `dev`, `ui` 
                    ''')

    # Main Logic App 
    st.title("Приложениее для поиска товаров")

    if 'df' not in st.session_state:
        st.session_state.df = load_df()

    # Логика работы с ml моделью
    model = load_model()
    search_df = model.search(product_id)
    
    # Логика отображения
    st.text('Найденный продукт:')
    # Заглушка для примера
    pred = st.session_state.df.sample().to_dict(orient='records')[0]
    st.write(pred)
    
    st.text('Топ 5 самых похожих продуктов:')
    # Заглушка для примера
    st.dataframe(search_df, hide_index=True)

if __name__ == '__main__':
    main()