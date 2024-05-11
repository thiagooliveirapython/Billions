import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import fundamentus as fd
from modelo import *

st.set_page_config(layout="wide")

text_css = """
    .st-Text {
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 1.5;
        white-space: pre-wrap;
        overflow-wrap: break-word;
        padding: 10px;
        border: 1px solid #eee;
        border-radius: 5px;
        margin-bottom: 20px;
    }
"""

def testa_chave(chave):
    if chave:
        resultado = genai.list_models()
        try:
            if resultado:
                for m in resultado:
                    if 'embedContent' in m.supported_generation_methods:
                        st.sidebar.success('Conexão bem-sucedida!')
                        return chave
        except Exception as e:
            st.error(f'Erro na conexão: {e}')
            st.error(f'Insira uma API_KEY válida')
            st.markdown('Você ainda não possui uma API_KEY? Crie uma agora mesmo! É muito fácil!')
            st.markdown('Basta ir no site abaixo e clicar em CREATE API_KEY')
            st.markdown('https://aistudio.google.com/app/apikey')
            return 'erro'
    else:
        st.warning('Insira uma chave de API no menu lateral.')
        st.markdown('Você ainda não possui uma API_KEY? Crie uma agora mesmo! É muito fácil!')
        st.markdown('Basta ir no site abaixo e clicar em CREATE API_KEY')
        st.markdown('https://aistudio.google.com/app/apikey')
        return "erro"


def cria_modelo(chave):

    modelo = ModeloGenerativo(
        model_name='gemini-1.5-pro-latest',
        api_key=chave,
        temperature=0.5,
    )
    return modelo


def home(chave):
    st.markdown('---')
    st.title('Billions')
    st.markdown('---')

    with st.form(key='form1'):
        prompt = st.text_input('Escreva o nome de uma empresa ou pergunte algo relacionado ao mercado financeiro. Exemplo: Petrobrás. Você também pode se divertir tentando fazer o chatbot falar sobre outros assuntos, mas ele só pensa em negócios')

        if prompt == "":
            st.warning('Você deve escrever algo')
        else:
            modelo = cria_modelo(chave)
            texto_gerado = modelo.gerar_texto(prompt=prompt)
            st.markdown(f"<p class='st-Text'>{texto_gerado}</p>", unsafe_allow_html=True)
            #st.text(texto_gerado)
        st.form_submit_button('Enviar')


    with st.form(key='form2'):
        ativo = st.text_input('Escreva aqui o TICKER do ativo que deseja buscar no yahoo finance.Exemplo: PETR4.SA ou GOOG. Vamos trazer um gráfico diário e algumas informações sobre a diretoria da empresa.')
        buscar = st.form_submit_button('Buscar')
        if buscar:
            # Verifica se a lista de ações não está vazia
            if ativo:
                try:
                    # Itera sobre cada ação e busca os dados históricos
                    hist_ativo = yf.download(ativo, start='2020-01-01', interval='1d')
                    if len(hist_ativo) == 0:
                        st.error(f"Ativo não encontrado")
                    else:
                        papel = yf.Ticker(ativo)
                        fig = go.Figure(data=[go.Candlestick(x=hist_ativo.index,
                                                             open=hist_ativo['Open'],
                                                             high=hist_ativo['High'],
                                                             low=hist_ativo['Low'],
                                                             close=hist_ativo['Close'],
                                                             name='Candles')])
                        fig.update_layout(title=ativo, xaxis_rangeslider_visible=False)
                        st.plotly_chart(fig, use_container_width=True)

                        modelo_info = cria_modelo(chave)
                        texto_gerado_info = modelo_info.gerar_texto(prompt=f"Fale o nome de todos os diretores conforme está aqui: {papel.info}. Procure falar coisas que ainda não tenha falado")
                        st.markdown(f"<p class='st-Text'>{texto_gerado_info}</p>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Ocorreu um erro ao baixar os dados: {e}")
            else:
                st.warning("Nenhuma ação fornecida. Por favor, insira pelo menos uma ação.")


def analise_fundamentalista(chave):
    st.markdown('---')
    st.title('Análise Fundamentalista de centenas de ativos')
    st.markdown('---')

    lista_tickers = fd.list_papel_all()
    papel1 = st.selectbox('Selecione o Papel', lista_tickers)
    info_papel1 = fd.get_detalhes_papel(papel1)
    pergunta = st.text_input(f'Analisei neste exato momento os dados Fundamenlistas de {papel1} através da API da Fundamentus! Pergunte algo!', value=" ")
    modelo3 = cria_modelo(chave)
    buscar3 = st.button('Fale mais')
    if buscar3:
        st.write(info_papel1)
        data_csv = info_papel1.to_csv(index=False)
        texto_gerado3 = modelo3.gerar_texto(prompt=f"responda a {pergunta} com base nestes dados{data_csv}. Procure falar coisas que ainda não tenha falado")
        st.markdown(f"<p class='st-Text'>{texto_gerado3}</p>", unsafe_allow_html=True)

def main():
    st.sidebar.title('Billions')
    st.sidebar.link_button("Instagram", "https://www.instagram.com/thiagooliveira.python/")
    st.sidebar.link_button("LinkedIn", "https://www.linkedin.com/in/thiago-oliveira-a1356723a/")
    st.sidebar.markdown('---')
    lista_menu=['Conheça os ativos', 'Análise Fundamentalista']
    escolha = st.sidebar.radio('Escolha a opção', lista_menu)
    chave = st.sidebar.text_input('insira sua API_KEY', type="password")

    genai.configure(api_key=chave)

    if escolha =='Conheça os ativos':
        chave = testa_chave(chave)
        if chave == "erro":
            pass
        else:
            home(chave)

    if escolha =='Análise Fundamentalista':
        chave = testa_chave(chave)
        if chave == "erro":
            pass
        else:
            analise_fundamentalista(chave)

main()
