## 2. The Scenario ##

import pandas as pd

playstore = pd.read_csv("googleplaystore.csv")
print(playstore.shape)

answer = 'no'

playstore = playstore.drop([10472], axis=0)

print(playstore.shape)

## 3. Cleaning the Data ##

def clean_size(size):
    """Convert file size string to float and megabytes"""
    size = size.replace("M","")
    if size.endswith("k"):
        size = float(size[:-1])/1000
    elif size == "Varies with device":
        size = pd.np.NaN
    else:
        size = float(size)
    return size

t = paid['Type'].head()

#droping the Type col from paid:
paid = paid.drop(['Type'], axis=1)
#paid.info()

#changing the Reviews col type to int:
paid['Reviews'] = paid['Reviews'].astype('int')
#paid.info()

paid['Size'] = paid['Size'].apply(clean_size)
paid.info()

## 4. Removing Duplicates ##

print(paid.columns)

print(
    'nº de linhas: {}'.format(paid.shape[0])
     )

paid.drop_duplicates(inplace=True)

print(
    'nº de linhas dp de dropar duplicados: {}'.format(paid.shape[0])
     )

#Checar qtas apps existem em duplicado:
print('nº de Apps duplicadas: {}'.format(paid.duplicated(subset='App').sum()))

paid = paid.sort_values(by='Reviews', ascending=False).copy()


#quais as apps duplicadas no N/DataFrame:
app_duple = paid[paid.duplicated(subset='App')]
#fzr um print d algumas 2 apps em duplicado:
print(paid[paid['App'] == 'Minecraft'])
print(paid[paid['App'] == 'Camera FV-5'])

#remover as apps duplicadas:
paid = paid.drop_duplicates(subset='App', keep='first').copy()

#Checar qtas apps existem em duplicado AGORA:
print(
    'nº de Apps duplicadas agora, dp da formatação:            {}'.format(paid.duplicated(subset='App').sum())
     )

#Fzr um reset ao index do DataFrame paid, de forma a dropar o index original:
paid.reset_index(drop=True, inplace=True) 

## 5. Exploring the Price ##

affordable_apps = paid[paid["Price"]<50].copy()

a = affordable_apps.sort_values(by='Price', ascending=False).copy()

#Apps, from the affordable_apps DF, that cost less than 5 USD:
cheap = affordable_apps['Price']<5
#Apps, from the affordable_apps DF, that cost 5 or more USD:
reasonable = affordable_apps['Price']>=5

affordable_apps[cheap].hist(column='Price', figsize=(12,6), grid=False)

affordable_apps[reasonable].hist(column='Price', color='orange', figsize=(12,6), grid=False)

#affordable_apps['affordability'] = affordable_apps[(affordable_apps['Price'] < 5 == 'cheap') & (affordable_apps['Price'] >= 5 == 'reasonable')]

#affordable_apps['affordability'] = affordable_apps[affordable_apps['Price'] > 5] == 'cheap'

affordable_apps.loc[affordable_apps['Price'] < 5, 'affordability'] = 'cheap' 
                                                       
affordable_apps.loc[affordable_apps['Price'] >= 5, 'affordability'] = 'reasonable'



## 6. Price vs. Rating ##

cheap = affordable_apps["Price"] < 5
reasonable = affordable_apps["Price"] >= 5

c = affordable_apps[cheap]

cheap_mean = affordable_apps[cheap]['Price'].mean()

print(cheap_mean)

affordable_apps.loc[cheap, 'price_criterion'] = affordable_apps['Price'].apply(lambda x: 1 if x < cheap_mean else 0)

affordable_apps[reasonable].plot(kind='scatter', x='Price', y='Rating')

Pearson_corr_coef = affordable_apps[reasonable].corr().loc['Price', 'Rating']
print(Pearson_corr_coef)

reasonable_mean = affordable_apps[reasonable]['Price'].mean()
print(reasonable_mean)

affordable_apps.loc[reasonable, 'price_criterion'] = affordable_apps[reasonable]['Price'].apply(lambda x: 1 if x < reasonable_mean else 0)

#print(affordable_apps['price_criterion'].head(10))
#print(affordable_apps['Price'].head(10))


#affordable_apps.loc[(affordable_apps[cheap]['Price'] < cheap_mean) | (affordable_apps[reasonable]['Price'] < reasonable_mean), 'price_criterion'] = 1

#affordable_apps.loc[(affordable_apps[cheap]['Price'] > cheap_mean) | (affordable_apps[reasonable]['Price'] > reasonable_mean), 'price_criterion'] = 0

print(affordable_apps['price_criterion'].head(10))
print(affordable_apps['Price'].head(10))

## 7. Price vs Category and Genres ##

affordable_apps["genre_count"] = affordable_apps["Genres"].str.count(";")+1

genres_mean = affordable_apps.groupby(
    ["affordability", "genre_count"]
).mean()[["Price"]]


def label_genres(row):
    """For each segment in `genres_mean`,
    labels the apps that cost less than its segment's mean with `1`
    and the others with `0`."""

    aff = row["affordability"]
    gc = row["genre_count"]
    price = row["Price"]

    if price < genres_mean.loc[(aff, gc)][0]:
        return 1
    else:
        return 0

affordable_apps["genre_criterion"] = affordable_apps.apply(
    label_genres, axis="columns"
)

#print(affordable_apps['genre_count'].head())

genres_mEan = affordable_apps.groupby(['Genres', 'affordability']).mean()[['Price']]

print(genres_mEan.head())

categories_mean = affordable_apps.groupby(['affordability', 'Category']).mean()[['Price']]

print(categories_mean.head())


def cat_label(row):
    
    afford = row['affordability']
    cat = row['Category']
    prc = row['Price']
    
    if prc < categories_mean.loc[(afford, cat)][0]:
        return 1
    else:
        return 0

affordable_apps['category_criterion'] = affordable_apps.apply(cat_label, axis='columns')

print(affordable_apps['category_criterion'].head())

## 8. Results and Impact ##

criteria = ["price_criterion", "genre_criterion", "category_criterion"]
affordable_apps["Result"] = affordable_apps[criteria].mode(axis='columns')


affordable_apps.loc[cheap, 'New Price'] =  round(affordable_apps['Price'].apply(lambda price: cheap_mean if price < cheap_mean else price), 2)

affordable_apps.loc[reasonable, 'New Price'] = round(affordable_apps['Price'].apply(lambda price: reasonable_mean if price < reasonable_mean else price), 2)

print(affordable_apps['New Price'].head(10))

print(affordable_apps['Price'].head(10))

affordable_apps['Installs'] = affordable_apps['Installs'].str.replace('+', '').copy()
affordable_apps['Installs'] = affordable_apps['Installs'].str.replace(',', '').copy()

affordable_apps['Installs'] =  affordable_apps['Installs'].astype(int).copy()
print(affordable_apps['Installs'].dtype)


affordable_apps['Impact'] = (affordable_apps['New Price'] - affordable_apps['Price'])*affordable_apps['Installs']

total_impact = affordable_apps['Impact'].sum()

print(total_impact)