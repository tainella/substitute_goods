import pandas as pd
import streamlit as st

from model.model import MyModel

@st.cache_resource()
def load_model(df_path: str = 'data/with_clusters.csv', n: int = 5) -> MyModel:
    """Логика загрузки модели машинного обучения.

    Args:
        df_path (str, optional): Путь до датафрейма в котором будет производится поиск. Defaults to 'path/to/df'.
        n (int, optional): Количество соседей в методе юлижайших соседей для алгоритма кластеризации. Defaults to 5. 

    Returns:
        MyModel: Загруженная модель.
    """
    return MyModel(df_path, n)


def load_df(df_path: str = 'data/worked_data.csv') -> pd.DataFrame:
    """Логика загрузки датафрейма в страницу.

    Args:
        df_path (str, optional): Путь до базового датафрейма. Defaults to 'data/worked_data.csv'.

    Returns:
        pd.DataFrame: Предобработанный датафрейм.
    """
    df = pd.read_csv(df_path)
    df = df.drop(columns = ['Unnamed: 0'])
    df = df[df['name'].notna()]
    return df


def prod_id_to_dict(df: pd.DataFrame, id: str) -> dict:
    """Преобразование id продукта к словарю с его свойствами из датафрейма.

    Args:
        df (pd.DataFrame): Датафрейм из которого будет искаться продукт.
        id (str): ID продукта (должен присутствовать в датафрейме).

    Returns:
        dict: _description_
    """
    if id in df['product_id'].values:
        result = df[df['product_id'] == id].drop(columns = ['product_id'])
        result = result.to_dict(orient='records')[0]
    else:
        result = {}
    return result


def find_product_id(name: str, kitchen: str, geohash: str, df: pd.DataFrame) -> str:
    """Поиск ID продукта исходя из его описания (работает только если такое сочетание признаков существует).

    Args:
        name (str): Имя продукта.
        kitchen (str): К какой кухне принадлежит.
        geohash (str): К какому геохешу принадлежит.
        df (pd.DataFrame): Датафрейм в котором будем искать id.

    Returns:
        str: id продукта.
    """
    pred1 = df['geohash'] == geohash
    pred2 = df['primary_cuisine'] == kitchen
    pred3 = df['en_name'] == name
    result = df[pred1 & pred2 & pred3]['product_id'].tolist()
    if len(result) != 0:
        return result[0]
    else:
        return None


def main():
    if 'df' not in st.session_state:
        st.session_state.df = load_df()
        st.session_state.geohash = sorted(st.session_state.df['geohash'].unique().tolist())
        st.session_state.kitchen = sorted(st.session_state.df['primary_cuisine'].unique().tolist())
        st.session_state.product = sorted(st.session_state.df['en_name'].unique().tolist())
    
    # Sidebar Search
    form = st.sidebar.form(key='Search')
    form.header("Поисковый запрос")

    geohash_search = form.selectbox('Выберите геохэш еды:', st.session_state.geohash)
    kitchen_search = form.selectbox('Выберите кухню:', st.session_state.kitchen)
    name_search = form.selectbox('Выберите название блюда:', st.session_state.product)
    
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
    st.title("Приложениее для поиска товаров-заменителей")

    # Логика отображения
    # Продукт, найденный по критериям поиска
    st.text('Найденный продукт:')
    product_id = find_product_id(name_search, kitchen_search, geohash_search, st.session_state.df)
    if product_id is not None:
        pred = prod_id_to_dict(st.session_state.df, product_id)
        st.write(pred)
        
        # Поиск товаров заменителей
        model = load_model()
        search_list = model.search(product_id) 
        search_df = st.session_state.df[st.session_state.df['product_id'].isin(search_list)].drop(columns = ['product_id'])
        
        st.divider()
        st.text('Топ 5 самых похожих продуктов:')
        st.dataframe(search_df, hide_index=True)
    else:
        st.markdown(f'''Продукт с параметрами 
                    \ngeohash:`{geohash_search}`
                   \nkitchen:`{kitchen_search}`
                   \nproduct name:`{name_search}`
                   \nне найден в базе данных!''')


if __name__ == '__main__':
    main()