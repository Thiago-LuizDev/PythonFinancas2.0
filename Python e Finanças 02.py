#!/usr/bin/env python
# coding: utf-8

# ### Exemplo: No nosso caso, vamos ver a performance de uma carteira de ativos. Vamos chamar de carteira do Lira.
# 
# - Temos o arquivo 'Carteira.xlsx' com os ativos e suas respectivas quantidades
# - Vamos analisar como que os ativos performaram, quanto que rendeu a carteira como um todo e comparar com o IBOV

# In[21]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import yfinance as yf

carteira = pd.read_excel('Carteira.xlsx')
display(carteira)


# ### Criando nosso dataframe de Cotações dos ativos da carteira

# In[27]:


cotacoes_carteira = pd.DataFrame()

for ativo in carteira['Ativos']:
    ticker = yf.Ticker(f'{ativo}.SA')
    dados_historicos = ticker.history(start='2023-01-01', end='2023-06-27')
    cotacoes_carteira[ativo] = dados_historicos['Close']

display(cotacoes_carteira)


# ### Será que todos os dados vieram corretos?

# In[28]:


cotacoes_carteira.info()


# ### Ajustando os dados

# In[29]:


#df_media = cotacoes_carteira.mean()
#cotacoes_carteira = cotacoes_carteira.fillna(df_media)
cotacoes_carteira = cotacoes_carteira.ffill()
cotacoes_carteira.info()


# ### Vamos ver como que as ações foram individualmente

# In[30]:


carteira_norm = cotacoes_carteira / cotacoes_carteira.iloc[0]
carteira_norm.plot(figsize=(15, 5))
plt.legend(loc='upper left')


# ### Vamos puxar o IBOV para comparar

# In[34]:


start_date = '2023-01-01'
end_date = '2023-06-27'
ticker = '^BVSP'

cotacao_ibov = yf.download(ticker, start=start_date, end=end_date)
display(cotacao_ibov)


# ### Criando um dataframe da Carteira com as quantidades de ações

# In[39]:


valor_investido = pd.DataFrame()

for ativo in carteira['Ativos']:
    valor_investido[ativo] = cotacoes_carteira[ativo] * carteira.loc[carteira['Ativos']==ativo, 'Qtde'].values[0]
display(valor_investido)    


# ### Comparação Carteira x IBOV

# In[43]:


valor_investido['Total'] = valor_investido.sum(axis=1)

valor_investido_norm = valor_investido / valor_investido.iloc[0]
cotacao_ibov_norm = cotacao_ibov / cotacao_ibov.iloc[0]

valor_investido_norm['Total'].plot(figsize=(15, 5), label='Carteira')
cotacao_ibov_norm['Adj Close'].plot(label='IBOV')
plt.legend()
plt.show()


# In[46]:


retorno_carteira = valor_investido['Total'][-1] / valor_investido['Total'][0] - 1
retorno_ibov = cotacao_ibov['Adj Close'][-1] / cotacao_ibov['Adj Close'][0] - 1
print(f'Retorno da Carteira: {retorno_carteira:.2%}')
print(f'Retorno IBOV: {retorno_ibov:.2%}')


# ### Correlação da Carteira com o IBOV

# In[47]:


correlacao = valor_investido['Total'].corr(cotacao_ibov['Adj Close'])
print(correlacao)

