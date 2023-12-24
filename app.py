import streamlit as st

st.title("Приложениее для поиска товаров")

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
