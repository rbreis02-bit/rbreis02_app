import streamlit as st
import pandas as pd
import plotly.express as px # Importando Plotly para o gráfico

# --- Configurações ---
NOME_ARQUIVO = 'custos.xlsx'
COLUNA_GRUPO_PLANEJAMENTO = 'Grp.planej.manutenç.'
COLUNA_VALOR = 'Valor'
COLUNA_SUPERINTENDENCIA = 'Superintendência' # Nova coluna para o gráfico

# 1. Configurar o layout da página para "wide" (largura total)
st.set_page_config(layout="wide", page_title="Análise de Custos com Gráfico")
st.title("Análise de Custos: Subtotal e Distribuição")

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
    st.metric(
        label=f"Subtotal de Gastos para {grupo_selecionado}",
        value=f"R$ {subtotal_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    
    st.markdown("---")
    
    # 8. Análise de Distribuição (Novo Passo)
    st.header(f"Distribuição de Gastos por {COLUNA_SUPERINTENDENCIA}")
    
    # Agrupar os dados filtrados por Superintendência e somar os valores
    gastos_por_super = df_filtrado.groupby(COLUNA_SUPERINTENDENCIA)[COLUNA_VALOR].sum().reset_index()
    gastos_por_super.columns = [COLUNA_SUPERINTENDENCIA, 'Total Gasto']
    
    # Criar o gráfico de barras interativo com Plotly
    fig = px.bar(
        gastos_por_super.sort_values(by='Total Gasto', ascending=False),
        x='Total Gasto',
        y=COLUNA_SUPERINTENDENCIA,
        orientation='h',
        title=f'Gastos por Superintendência em {grupo_selecionado}',
        labels={'Total Gasto': 'Total Gasto (R$)', COLUNA_SUPERINTENDENCIA: 'Superintendência'},
        height=500
    )
    
    # Exibir o gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 9. Exibir a Tabela de Detalhes
    st.subheader(f"Detalhes dos Registros: {grupo_selecionado}")
    st.write(f"Total de registros: {len(df_filtrado)}")
    st.dataframe(df_filtrado, use_container_width=True)
    
except FileNotFoundError:
    st.error(f"ERRO: O arquivo '{NOME_ARQUIVO}' não foi encontrado.")
    st.info("Verifique se o arquivo está na mesma pasta do seu script.")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar ou processar a planilha: {e}")
