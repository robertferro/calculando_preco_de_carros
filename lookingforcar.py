import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np


st.set_page_config(page_title = 'Looking For Car', 
				   layout = 'wide', 
				   initial_sidebar_state = 'auto')


st.title('Looking For Car')

url = 'https://raw.githubusercontent.com/robertferro/carros_populares/main/3%20-%20EDA/carros_populares_filtrados.csv'
dados_raw=pd.read_csv(url,sep=',')


# encoding das variaveis
dados=dados_raw.copy()
marcas = list(dados.sort_values('marca').marca.unique())
num_marcas = list(np.arange(1,14))
dic_marcas = dict(zip(marcas, num_marcas))
dados['marca'] = dados['marca'].map(dic_marcas)


modelos = list(dados.sort_values('modelo').modelo.unique())
modelos_num = list(np.arange(1,125))
dic_modelos = dict(zip(modelos, modelos_num))
dados['modelo'] = dados['modelo'].map(dic_modelos)

# Machine learning

dados_ml=dados.copy()
X=dados_ml.drop(columns=['preco','informacoes'],axis=1)
y=dados_ml['preco']

X_treino, X_teste, y_treino,y_teste=train_test_split(X,y,test_size=0.25,stratify=dados['marca'],shuffle=True,random_state=0)
reg = RandomForestRegressor(n_estimators=500, min_samples_leaf=2,random_state=42)
reg.fit(X_treino,y_treino)

# script streamlit

paginas=['Home','Banco de Dados','Avaliação']
st.sidebar.markdown('## **Selecione a opção desejada**')
pagina=st.sidebar.selectbox('',paginas)
# page1
if pagina=='Home':
	st.markdown('## Surgiu aquela dúvida na hora de avaliar seu carro usado ?! A gente te ajuda !!!')
	st.write('## Quer fazer uma busca rápida sobre carros usados?! Também podemos te ajudar com isso!')
	imagem='img.jpg'
	st.image(imagem,use_column_width='always')
# page2
if pagina=='Banco de Dados':
	st.write('**Aqui temos alguns registros de veículos das mais variadas marcas e modelos.**')
	st.write('**Os dados exibidos aqui foram coletados via web e trazem valores propostos por usuários quando estão negociando seus carros.**')
	st.write('**Faça uma busca em nossa base de dados interagindo com os widgets abaixo!!!**')	
	dados=dados_raw.copy()
	marcas=list(dados.sort_values('marca').marca.unique())
	marca=st.selectbox('Marca',marcas)
	df=dados.copy()
	df = df[df['marca']==marca]
	modelos=list(df.sort_values('modelo').modelo.unique())
	modelo=st.selectbox('Modelo',modelos)
	df = df[df['modelo']==modelo]
	ano=st.selectbox('Selecione o ano do carro',list(df.sort_values('ano').ano.unique()))
	st.markdown('---')
	st.write(df)


# page3
if pagina=='Avaliação':

	marcas=list(dados_raw.sort_values('marca').marca.unique())
	marca=st.selectbox('Marca',marcas)
	df = dados_raw[dados_raw['marca']==marca]
	modelos=list(df.sort_values('modelo').modelo.unique())
	modelo=st.selectbox('Modelo',modelos)
	df = df[df['modelo']==modelo]
	ano=st.number_input('Digite o ano do veículo')
	motor=st.selectbox('Escolha a potência do motor do veículo',list(df.sort_values('motor').motor.unique()))
	km=st.number_input('Digite a quilometragem do veículo')


	
	# Criando um dataframe para entrada do modelo 
	dicionario  =  {'marca':[marca], 
			  'modelo':[modelo],
			  'motor':[motor], 
			  'quilometragem':[km],
	       	  'ano':[ano]
	       	  	}


	dados_entrada = pd.DataFrame(dicionario)
	st.write(dados_entrada)


	# Encoding das variaveis categoricas do dataframe

	marcas = list(dados_raw.sort_values('marca').marca.unique())
	num_marcas = list(np.arange(1,14))
	dic_marcas = dict(zip(marcas, num_marcas))
	dados_entrada['marca'] = dados_entrada['marca'].map(dic_marcas)

	modelos = list(dados_raw.sort_values('modelo').modelo.unique())
	modelos_num = list(np.arange(1,125))
	dic_modelos = dict(zip(modelos, modelos_num))
	dados_entrada['modelo'] = dados_entrada['modelo'].map(dic_modelos)

	st.markdown('---')

	

	if st.button('Executar a Simulação'):
		previsao=list(reg.predict(dados_entrada).round(2))[0]
		st.markdown(' **O veículo foi avaliado em: R$** {}'.format(previsao))
