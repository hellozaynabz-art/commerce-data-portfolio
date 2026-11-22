"""Retail revenue, credits, and observed repeat purchasing; no causal uplift claims."""
import sys, sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import retail, dump
import pandas as pd
ROOT=Path(__file__).resolve().parent

def run():
 raw,clean,sales,source=retail()
 # Use complete Jan-Nov months for commercial reporting and cohort observations.
 clean=clean[clean.InvoiceDate.between('2011-01-01','2011-11-30 23:59:59')].copy()
 sales=sales[sales.InvoiceDate.between('2011-01-01','2011-11-30 23:59:59')].copy()
 clean['region']=clean.Country.eq('United Kingdom').map({True:'United Kingdom',False:'International'})
 sales['region']=sales.Country.eq('United Kingdom').map({True:'United Kingdom',False:'International'})
 conn=sqlite3.connect(':memory:');clean.to_sql('lines',conn,index=False)
 query=(ROOT/'metrics.sql').read_text()
 monthly=pd.read_sql_query(query,conn)
 monthly.to_csv(ROOT/'monthly-revenue.csv',index=False)
 known=sales.dropna(subset=['CustomerID']).copy()
 customers=known.groupby('CustomerID').agg(orders=('InvoiceNo','nunique'),last=('InvoiceDate','max'),gross=('amount','sum'))
 customers['recency']=(pd.Timestamp('2011-12-01')-customers['last']).dt.days
 customers['segment']=['Active repeat' if r<=60 and f>=2 else 'Lapsed repeat' if f>=2 else 'Recent one-time' if r<=60 else 'Dormant one-time' for r,f in zip(customers.recency,customers.orders)]
 segments=customers.groupby('segment').agg(customers=('orders','size'),gross=('gross','sum')).reset_index()
 segments.to_csv(ROOT/'customer-segments.csv',index=False)
 known['cohort']=known.groupby('CustomerID').month.transform('min')
 known['age']=(known.InvoiceDate.dt.year*12+known.InvoiceDate.dt.month)-(pd.to_datetime(known.cohort).dt.year*12+pd.to_datetime(known.cohort).dt.month)
 co=known.groupby(['cohort','age']).CustomerID.nunique().reset_index(name='customers')
 sizes=co[co.age.eq(0)].set_index('cohort').customers
 co['rate']=co.customers/co.cohort.map(sizes)
 co.to_csv(ROOT/'cohort-retention.csv',index=False)
 months=sorted(sales.month.unique())
 known_month1=co[co.age.eq(1)]
 total_gross=float(sales.amount.sum());credits=float(-clean.loc[clean.amount.lt(0),'amount'].sum())
 summary={'gross_sales':total_gross,'credit_value':credits,'net_sales':float(clean.amount.sum()),'orders':int(sales.InvoiceNo.nunique()),'known_customers':len(customers),'repeat_share':float(customers.orders.ge(2).mean()),'identified_revenue_share':float(known.amount.sum()/total_gross),'credit_to_gross':credits/total_gross,'period':'Jan–Nov 2011','raw_rows':len(raw),'duplicate_rows':int(raw.duplicated().sum()),'missing_customer_rows':int(raw.CustomerID.isna().sum()),'filtered_lines':len(clean),'first_return_rate':float(known_month1.customers.sum()/sizes.loc[known_month1.cohort].sum())}
 top=sales.groupby(['StockCode','Description'],dropna=False).agg(gross=('amount','sum'),units=('Quantity','sum')).reset_index().sort_values('gross',ascending=False).head(10)
 top.to_csv(ROOT/'top-products.csv',index=False)
 payload={'summary':summary,'monthly':monthly.round(2).to_dict('records'),'segments':segments.round(2).to_dict('records'),'cohorts':co.to_dict('records'),'top_products':top.round(2).to_dict('records')}
 dump(ROOT/'results.json',payload)
 assert abs(monthly.net_sales.sum()-summary['net_sales'])<.01
 assert int(segments.customers.sum())==summary['known_customers']
 assert (co.rate.between(0,1)).all()
 print('Revenue:',summary)
 return payload
if __name__=='__main__':run()
