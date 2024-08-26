## 2. What's a Good Metric? ##

ans1 = 'no'

ans21 = 'no'

ans22 = 'yes'

## 3. Introduction to the Net Promoter Score ##

def categorize (score):
    if score >= 0 and score <= 6:
        return 'Detractor'
    elif score >= 7 and score <=8:
        return 'Passive'
    else:
        return 'Promoter'
    
print(categorize(11))

    

## 4. Net Promoter Score ##

import pandas as pd

df = pd.read_csv("nps.csv", parse_dates=["event_date"])

#https://www.delftstack.com/howto/python-pandas/how-to-extract-month-and-year-separately-from-datetime-column-in-pandas/
# Umas das formas de sacar de uma datetime Series quer o Mês quer o Ano é usar o data acesor dt.strftime. Transformamos assim o Ano ou o Mês numa string:
year= df['event_date'].dt.strftime('%Y')
month =df['event_date'].dt.strftime('%m')

    #year = df['event_date'].dt.year.astype('str')
    #month = df['event_date'].dt.month.astype('str')

    
#'Retransformar' a str Mês e Ano num integer, recorrendo à função incorporada astype():
df['yearmonth'] = (year+month).astype(int)
print(year+month)

#Outra das formas de sacar o Mês ou Ano é usar o datetime acesor dt.to_period() e depois selecionar 'M' para Mês ou 'Y' para ano:
    #df['yearmonth'] = df['event_date'].dt.to_period('M')
    #print(df['yearmonth'].head())
    #print(df['yearmonth'].dtype)
    


df['category'] = df['score'].apply(categorize)
print(df['category'].sample(5))

#Criar agora uma tabela pivot c o index constituido pela info respeitante ao Ano e Mês em q os surveys foram preenchidos, as colunas serão as categorias dadas de acordo com o q os users votaram: Detractor; Passive e Promoter. E agregar essas linhas pelo tamanho, ou seja, pelo nº de x com q ocorreram em determinado mês de determinado ano. Isto td a parir do DF df:
nps = pd.pivot_table(df, index=['yearmonth'], columns=['category'], aggfunc='size')

#Calcular o nmr de respostas para cada Mês, e inputar esse nmr à nova coluna total_responses:
nps['total_responses'] = nps[nps.columns].sum(axis=1)
#print(nps.columns)

#Dp d termos o nmr total de respostas, o nmr total para os Promoters e o nº total para os Detractors, é hora agora de calcular a percetagem de NPS's((Promoter-Detractor)/total_responses)):
nps['nps'] = (nps['Promoter'] - nps['Detractor'])/nps['total_responses']

nps['nps'] = (nps['nps']*100).astype(int).copy()

## 6. Customer Churn ##

import pandas as pd
#Ler o ficheiro muscle_labs.csv num DataFrame, recorrendo ao metodo read_csv, e fazer o parse das cols respeitante as datas:
subs = pd.read_csv('muscle_labs.csv', parse_dates=['end_date', 'start_date'])

#Sacar quer o Mes, quer o Ano de ambas as cols que cotem datas, e atribui-las as variaveis year e month. Ambas sao 'pescadas' atraves do metodo dt.strftime() e em strings:
year = subs['end_date'].dt.strftime('%Y')
month = subs['end_date'].dt.strftime('%m')

#Atribuir ambas as datas sacadas, Mes e Ano a col churn_month, e tranformar isso num objecto numerico, de uma str--int:
subs['churn_month'] = (year+month).astype(int)
print(subs.sample(5))

#Agrupar o DataFrame subs a partir da col churn_month, recorrendo ao metodo groupby(), e dp de o agrupar, usar a funçao agg para agregar essa info por uma coluna so, a id, e alem disso atribuir como valores a essa coluna id o nmr d amostras encontradas para cada row respeitante a cada churn_month:
monthly_churn = subs.groupby('churn_month').agg({'id':'size'}).copy()

#Depois do processo realizado acima, so nos resta uma coisa, alterar o nome da coluna id por total_churned. Recorremos ao metodo rename para isso:
monthly_churn = monthly_churn.rename(columns={'id':'total_churned'})

print(monthly_churn.sample(5))



## 7. Date Wrangling ##

years = list(range(2011,2015))
months = list(range(1,13))
yearmonths = [y*100+m for y in years for m in months]
yearmonths = yearmonths[:-1]

churn = pd.DataFrame({"yearmonth": yearmonths})

churn = pd.merge(churn, monthly_churn, how='left', left_on=['yearmonth'], right_index=True)

#print(churn.head(5))

churn = churn.fillna(0).copy()
#print(churn.head(5))

churn['total_churned'] = churn['total_churned'].astype(int).copy()
print(churn.head(5))




## 8. Churn Rate ##

import datetime as dt

# arange = __import__("numpy").arange
# Ellipse = __import__("matplotlib").patches.Ellipse
# ax = churn.plot(x="yearmonth", y="churn_rate", figsize=(12,6), rot=45, marker=".")
# start, end = ax.get_xlim()
# ax.get_xticks()
# ax.set_xticks(arange(2, end, 3))
# ax.set_xticklabels(yearmonths[2::3])
# circle = Ellipse((35, churn.loc[churn.yearmonth == "201312", "churn_rate"].iloc[0]),
#                  5, 0.065, color='sandybrown', fill=False
#                    )
# ax.add_artist(circle)
# ax.xaxis.label.set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.get_legend().remove()



import datetime as dt

# arange = __import__("numpy").arange
# Ellipse = __import__("matplotlib").patches.Ellipse
# ax = churn.plot(x="yearmonth", y="churn_rate", figsize=(12,6), rot=45, marker=".")
# start, end = ax.get_xlim()
# ax.get_xticks()
# ax.set_xticks(arange(2, end, 3))
# ax.set_xticklabels(yearmonths[2::3])
# circle = Ellipse((35, churn.loc[churn.yearmonth == "201312", "churn_rate"].iloc[0]),
#                  5, 0.065, color='sandybrown', fill=False
#                    )
# ax.add_artist(circle)
# ax.xaxis.label.set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.get_legend().remove()
import datetime as dt

def get_customers(yearmonth):
    year = yearmonth//100
    month = yearmonth-year*100
    date = dt.datetime(year, month, 1)
    
    return ((subs["start_date"] < date) & (date <= subs["end_date"])).sum()

churn["total_customers"] = churn["yearmonth"].apply(get_customers)
churn["churn_rate"] = churn["total_churned"] / churn["total_customers"]
churn["yearmonth"] = churn["yearmonth"].astype(str)

arange = __import__("numpy").arange
Ellipse = __import__("matplotlib").patches.Ellipse
ax = churn.plot(x="yearmonth", y="churn_rate", figsize=(12,6), rot=45, marker=".")
start, end = ax.get_xlim()
ax.get_xticks()
ax.set_xticks(arange(2, end, 3))
ax.set_xticklabels(yearmonths[2::3])
circle = Ellipse((35, churn.loc[churn.yearmonth == "201312", "churn_rate"].iloc[0]),
                 5, 0.065, color='sandybrown', fill=False
                   )
ax.add_artist(circle)
ax.xaxis.label.set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_legend().remove()