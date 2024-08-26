## 2. Communication is a Two-way Street ##

# ans = "A"
# ans = "B"
ans = "C"

## 3. Dealing with Fuzzy Language ##

ans = "A"
# ans = "B"
# ans = "C"

## 4. Churned Customers ##

import pandas as pd
import datetime as dt

data = pd.read_csv("rfm_xmas19.txt", parse_dates=["trans_date"])
group_by_customer = data.groupby("customer_id")
last_transaction = group_by_customer["trans_date"].max()

best_churn = pd.DataFrame(last_transaction)

cutoff_day = dt.datetime(2019,10,16)

def func_churned(n):
    if n < cutoff_day:
        return 1
    else:
        return 0
    

best_churn['churned'] = best_churn['trans_date'].apply(func_churned)

## 5. Aggregate Data by Customer ##

best_churn["nr_of_transactions"] = group_by_customer.size()

best_churn = best_churn.drop(['trans_date'], axis=1)

data_10 = data.sort_values(['customer_id'])

#best_churn['amount_spent'] = data['tran_amount']

#data.head()

data_10_grp = data_10.groupby('customer_id')

data_10_grp_total = data_10_grp['tran_amount'].sum()

a = best_churn.sort_index()
b = a.groupby(by=['customer_id'])

best_churn['amount_spent'] = data_10_grp_total

## 6. Ranking Customers ##

best_churn['scaled_tran'] = (best_churn['nr_of_transactions']-best_churn['nr_of_transactions'].min())/(best_churn['nr_of_transactions'].max()-best_churn['nr_of_transactions'].min())

best_churn['scaled_amount'] = (best_churn['amount_spent']-best_churn['amount_spent'].min())/(best_churn['amount_spent'].max()-best_churn['amount_spent'].min())

best_churn['score'] = 100*((0.5*best_churn['scaled_amount']) + (0.5*best_churn['scaled_tran']))

best_churn.sort_values(by=['score'], ascending=False, inplace=True)

print(best_churn.head())

## 7. Determining a Threshold ##

top_5 = data.head()

coupon = data['tran_amount'].mean()*0.3

nr_of_customers = 1000/coupon

## 8. Delivering the Results ##

top_50_churned = best_churn[best_churn['churned']==1].head(50)
#top_50_churned = best_churn.head(50)


top_50_churned.to_csv('best_customers.txt')

print(top_50_churned)