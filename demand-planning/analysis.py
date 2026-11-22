"""One-day-ahead unit-sales backtest. All features are shifted before the target."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import retail, dump
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
ROOT=Path(__file__).resolve().parent

def features(s):
 x=pd.DataFrame(index=s.index)
 for lag in (1,7,14,28):x[f'lag_{lag}']=s.shift(lag)
 for window in (7,28):x[f'mean_{window}']=s.shift(1).rolling(window).mean()
 x['weekday']=s.index.dayofweek;x['month']=s.index.month
 return x

def score(y,p):
 return {'mae':float(mean_absolute_error(y,p)),'wape':float(np.abs(y-p).sum()/np.abs(y).sum()),'bias_units':float(np.mean(p-y))}

def run():
 _,_,sales,_=retail()
 sales=sales[(sales.Country=='United Kingdom')&(sales.InvoiceDate<'2011-12-01')]
 # Select the five most frequently ordered SKUs using training data only.
 candidates=sales[sales.InvoiceDate<'2011-10-01'].groupby('StockCode').InvoiceNo.nunique().nlargest(5).index
 results=[];forecasts=[]
 for sku in candidates:
  part=sales[sales.StockCode==sku]
  s=part.groupby('date').Quantity.sum().reindex(pd.date_range('2010-12-01','2011-11-30'),fill_value=0).astype(float)
  x=features(s);ok=x.notna().all(axis=1);x=x[ok];y=s.loc[x.index]
  train=x.index<'2011-10-01';valid=(x.index>='2011-10-01')&(x.index<'2011-11-01');test=x.index>='2011-11-01'
  model=HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=7,l2_regularization=2,random_state=42)
  model.fit(x[train],y[train]);vp=np.maximum(0,model.predict(x[valid]))
  vm=score(y[valid].values,vp);vb=score(y[valid].values,x.loc[valid,'lag_7'].values)
  # Validation decides method. Refit only on pre-test data after selection.
  selected='Gradient boosting' if vm['mae']<vb['mae'] else 'Seasonal baseline'
  model.fit(x[~test],y[~test]);pred=np.maximum(0,model.predict(x[test]));baseline=x.loc[test,'lag_7'].values
  actual=y[test].values;chosen=pred if selected=='Gradient boosting' else baseline
  row={'sku':sku,'name':str(part.Description.mode().iloc[0]),'method':selected,'validation_ml':vm,'validation_baseline':vb,'model':score(actual,pred),'baseline':score(actual,baseline),'selected':score(actual,chosen),'train_days':int(train.sum()),'validation_days':int(valid.sum()),'test_days':int(test.sum())}
  results.append(row)
  for date,a,p,b,c in zip(x[test].index,actual,pred,baseline,chosen):
   forecasts.append({'sku':sku,'date':date.strftime('%Y-%m-%d'),'actual':float(a),'model':round(float(p),2),'baseline':float(b),'selected':round(float(c),2)})
 f=pd.DataFrame(forecasts);f.to_csv(ROOT/'backtest.csv',index=False)
 summary={'selected':score(f.actual.values,f.selected.values),'baseline':score(f.actual.values,f.baseline.values),'model':score(f.actual.values,f.model.values),'skus':len(results),'test_days':30,'test_start':'2011-11-01','test_end':'2011-11-30','ml_selected':sum(r['method']=='Gradient boosting' for r in results)}
 summary['mae_change']=1-summary['selected']['mae']/summary['baseline']['mae']
 payload={'summary':summary,'products':results,'forecasts':forecasts}
 dump(ROOT/'results.json',payload)
 assert f.shape[0]==150 and (f[['actual','model','baseline','selected']]>=0).all().all()
 print('Demand:',summary)
 return payload
if __name__=='__main__':run()
