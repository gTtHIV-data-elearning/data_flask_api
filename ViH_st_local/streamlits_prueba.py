import streamlit as st
import pandas as pd 
import matplotlib as plt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from PIL import Image
import seaborn as sns

import psycopg2
import streamlit as st

from sklearn.datasets import load_iris

#Cargar data iris y formar el data frame



@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets['postgres'])

conn=init_connection()

@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
rows=run_query('SELECT * FROM consumption')

Data=pd.DataFrame(rows)

iris = load_iris()
X = iris.data
y = iris.target

df=pd.DataFrame(X,columns=iris['feature_names'])
df['Type']=y

#Descarga de imagenes que se vayan a utilizar

img = Image.open('images/descarga.jpg')

#Estilizar la ventana de la aplicacion

# st.set_page_config(page_title='Evaluación',
#                   page_icon=':bar_chart:',
#                   layout='wide')

#Distribucion de las ventanas de trabajo 

menu = st.sidebar.selectbox("Selecciona la página", ['Inicio','Graficos 1','Graficos 2'])

#Primera ventana en donde se vera info de la app y datos rapidos

if menu == 'Inicio':
    
    df_especies=df['Type'].replace([0, 1, 2], ['setosa', 'versicolor','virginica'])
    df['Especies']=df_especies

    #parte escrita de la pagina inicio

    st.title('# Inicio')
    st.markdown('Aqui se explicara las funcionalidades de la aplicacion de manera breve para facilitar el uso a aquelllos administradores.')
    st.write(Data.head(50))

    opciones = ['Todos'] + df['Especies'].unique().tolist()

    # menu de seleccion para tipos de flores 

    menu = st.sidebar.selectbox('Selecciona una flor', opciones)

    # si se selecciona "Todos"

    if menu == 'Todos':
        # calcular totales y medias para todas las flores

        flores_totales=int(df['Especies'].count())
        media_largo= round(df['petal length (cm)'].mean(),2)
        media_ancho= round(df['petal width (cm)'].mean(),2)

        # mostrar resultados

        st.title(f'Ejemplo para {menu}')
        st.markdown('##')
        left_column, middle_column , right_column=st.columns(3)

        with left_column:
            st.subheader('Flores Totales')
            st.subheader(f':hibiscus:  {flores_totales:}')
        with middle_column:
            st.subheader('Media largo del petalo')
            st.subheader(f':arrow_up_down: {media_largo:}')
        with right_column:
            st.subheader('Media de ancho del petalo')
            st.subheader(f':left_right_arrow: {media_ancho:}')

    # si se selecciona una flor en especifico
    else:
        # filtrar el DataFrame por la flor seleccionada

        df_filtrado = df[df['Especies'] == menu]

        # calcular totales y medias para la flor seleccionada

        flores_totales=int(df_filtrado['Especies'].count())
        media_largo= round(df_filtrado['petal length (cm)'].mean(),2)
        media_ancho= round(df_filtrado['petal width (cm)'].mean(),2)

        # mostrar resultados

        st.title(f'Ejemplo para {menu}')
        st.markdown('##')
        left_column, middle_column , right_column=st.columns(3)

        with left_column:
            st.subheader('Flores Totales')
            st.subheader(f':hibiscus:  {flores_totales:}')
        with middle_column:
            st.subheader('Media largo del petalo')
            st.subheader(f':arrow_up_down: {media_largo:}')
        with right_column:
            st.subheader('Media de ancho del petalo')
            st.subheader(f':left_right_arrow: {media_ancho:}')

#En esta ventana se mostraran todos los graficos acerca de la clase en general. Aspectos Macro

elif menu == "Graficos 1": 
    df_especies=df['Type'].replace([0, 1, 2], ['setosa', 'versicolor','virginica'])
    df['Especies']=df_especies

    #creacion de menu seleccion de graficos

    graficos = st.selectbox('Selecciona una flor', ['Cantidad de flores', 'Distribucion de flores'])

    if graficos == 'Distribucion de flores':

        st.title('Distribucion de flores')
        st.markdown('##')
        fig1 = px.scatter(df, x='petal width (cm)', y='petal length (cm)',color='Especies', title=f'Distribución del pétalo')
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown('Debajo de cada grafica irá una breve exlpicacion de la tabla  ')


        fig2 = px.scatter(df, x='sepal width (cm)', y='sepal length (cm)',color='Especies',  title=f'Distribución del sépalo')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('Debajo de cada grafica irá una breve exlpicacion de la tabla  ')

    if graficos == 'Cantidad de flores':
        

        st.title("Cantidad de flores")

        left_column, middle_column , right_column=st.columns(3)

        with left_column:
            st.subheader('Setosa')
            st.subheader(str(df['Type'].value_counts()[0]))
        with middle_column:
            st.subheader('Versicolor')
            st.subheader(str(df['Type'].value_counts()[1]))
        with right_column:
            st.subheader('Virginica')
            st.subheader(str(df['Type'].value_counts()[2]))

        cantidad = df['Type'].value_counts(normalize=True)
        colors = sns.color_palette("Spectral").as_hex()


        fig_3 = px.pie(values = cantidad.values, names = ['Setosa', 'Versicolor', 'Virginica'], color_discrete_sequence=colors)
        st.plotly_chart(fig_3)

        st.markdown('Debajo de cada grafica irá una breve exlpicacion de la tabla  ')
    
    


elif menu == "Graficos 2":
    df_especies=df['Type'].replace([0, 1, 2], ['setosa', 'versicolor','virginica'])
    df['Especies']=df_especies

    flower_types = df['Especies'].unique()

    # Agregamos un widget selectbox para elegir el tipo de flor a visualizar
    selected_flower = st.selectbox('Selecciona una flor', flower_types)

    # Filtramos los datos del DataFrame para obtener solo las filas con la flor seleccionada
    selected_data = df[df['Especies'] == selected_flower]

    # Creamos un gráfico de pastel para la distribución de las longitudes del pétalo
    fig1 = px.histogram(selected_data, x='petal length (cm)', nbins=15, title=f'Distribución de longitudes de pétalo para {selected_flower}')
    st.plotly_chart(fig1, use_container_width=True)

    # Creamos un gráfico de pastel para la distribución de las anchuras del pétalo
    fig2 = px.histogram(selected_data, x='petal width (cm)', nbins=15, title=f'Distribución de anchuras de pétalo para {selected_flower}')
    st.plotly_chart(fig2, use_container_width=True)


