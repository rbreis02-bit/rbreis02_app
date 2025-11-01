mport streamlit as st
import pandas as pd

# --- Configurações ---
NOME_ARQUIVO = 'custos.xlsx'
COLUNA_GRUPO_PLANEJAMENTO = 'Grp.planej.manutenç.'
COLUNA_VALOR = 'Valor' # Adicionando a coluna Valor para o cálculo

# 1. Configurar o layout da página para "wide" (largura total)
st.set_page_config(layout="wide", page_title="Visualização de Custos com Filtro")
st.title("Visualização da Base de Dados de Custos com Filtro")

try:
    # 2. Carregar os dados
    df = pd.read_excel(NOME_ARQUIVO)
    
    # Garantir que a coluna de valor seja numérica para o cálculo
    df[COLUNA_VALOR] = pd.to_numeric(df[COLUNA_VALOR], errors='coerce')
    df.dropna(subset=[COLUNA_VALOR], inplace=True)
    
    st.success(f"Base de dados '{NOME_ARQUIVO}' carregada com sucesso!")
    
    # 3. Criar a lista de opções para o filtro
    opcoes_grupo = ['Todos'] + sorted(df[COLUNA_GRUPO_PLANEJAMENTO].unique().tolist())
    
    # 4. Criar o seletor (selectbox) na barra lateral
    st.sidebar.header("Filtros")
    grupo_selecionado = st.sidebar.selectbox(
        'Selecione o Grupo de Planejamento:',
        opcoes_grupo
    )
    
    # 5. Aplicar o filtro
    if grupo_selecionado == 'Todos':
        df_filtrado = df
    else:
        df_filtrado = df[df[COLUNA_GRUPO_PLANEJAMENTO] == grupo_selecionado]
        
    # 6. Calcular o Subtotal do Valor
    subtotal_valor = df_filtrado[COLUNA_VALOR].sum()
    
    # 7. Exibir o Subtotal em um Cartão (st.metric)
    # Usamos o formatador de moeda brasileira (R$)
    st.metric(
        label=f"Subtotal de Gastos para {grupo_selecionado}",
        value=f"R$ {subtotal_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    
    # 8. Exibir o restante do resultado
    st.subheader(f"Detalhes dos Registros: {grupo_selecionado}")
    st.write(f"Total de registros: {len(df_filtrado)}")
    
    # Exibir a tabela filtrada
    st.dataframe(df_filtrado, use_container_width=True)
    
except FileNotFoundError:
    st.error(f"ERRO: O arquivo '{NOME_ARQUIVO}' não foi encontrado.")
    st.info("Verifique se o arquivo está na mesma pasta do seu script.")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar ou processar a planilha: {e}")
