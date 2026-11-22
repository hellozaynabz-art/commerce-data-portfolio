"""Shared, reproducible data loading. Raw datasets stay out of Git."""
from pathlib import Path
import hashlib, io, json, zipfile
import pandas as pd
import requests
ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'data' / 'raw'
SOURCES = {
 'retail': {'url':'https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip','member':'Online Retail.xlsx','doi':'https://doi.org/10.24432/C5BW33','citation':'Chen, D. (2015). Online Retail. UCI Machine Learning Repository.','license':'CC BY 4.0'},
 'shoppers': {'url':'https://archive.ics.uci.edu/static/public/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset.zip','member':'online_shoppers_intention.csv','doi':'https://doi.org/10.24432/C5F88Q','citation':'Sakar, C. & Kastro, Y. (2018). Online Shoppers Purchasing Intention Dataset. UCI Machine Learning Repository.','license':'CC BY 4.0'}
}
def dump(path, obj):
 Path(path).write_text(json.dumps(obj, indent=2, allow_nan=False, default=lambda x: x.item() if hasattr(x,'item') else str(x))+'\n')
def load_data(name):
 RAW.mkdir(parents=True, exist_ok=True)
 source=SOURCES[name]; archive=RAW/f'{name}.zip'
 if not archive.exists():
  r=requests.get(source['url'],timeout=120);r.raise_for_status();archive.write_bytes(r.content)
 digest=hashlib.sha256(archive.read_bytes()).hexdigest()
 manifest=ROOT/'data-provenance.json'
 if manifest.exists():
  expected=json.loads(manifest.read_text()).get(name,{}).get('sha256')
  if expected and expected!=digest: raise ValueError('Dataset checksum changed; review before rebuilding')
 data=zipfile.ZipFile(archive).read(source['member'])
 df=pd.read_excel(io.BytesIO(data)) if name=='retail' else pd.read_csv(io.BytesIO(data))
 return df, {**source,'sha256':digest,'raw_rows':len(df)}
def retail():
 raw,source=load_data('retail')
 df=raw.drop_duplicates().copy()
 df['InvoiceNo']=df.InvoiceNo.astype(str);df['StockCode']=df.StockCode.astype(str)
 df['InvoiceDate']=pd.to_datetime(df.InvoiceDate)
 df['date']=df.InvoiceDate.dt.normalize()
 # Exclude service/manual/non-product codes, free items, zero quantity. Retain signed credits.
 valid=df.StockCode.str.match(r'^\d{5}[A-Za-z]?$') & df.UnitPrice.gt(0) & df.Quantity.ne(0)
 df=df.loc[valid].copy();df['amount']=df.Quantity*df.UnitPrice
 df['month']=df.InvoiceDate.dt.strftime('%Y-%m')
 df['cancel']=df.InvoiceNo.str.upper().str.startswith('C')
 positive=df[(df.Quantity>0)&(~df.cancel)].copy()
 return raw,df,positive,source
if __name__=='__main__':
 provenance={}
 for name in SOURCES:
  _,provenance[name]=load_data(name)
 dump(ROOT/'data-provenance.json',provenance)
 print({k:{'rows':v['raw_rows'],'sha256':v['sha256']} for k,v in provenance.items()})
