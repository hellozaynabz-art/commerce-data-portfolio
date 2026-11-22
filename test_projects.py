"""Meaningful checks of reconciliation, time leakage, and published evidence."""
import unittest, json, runpy, math
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import pandas as pd
import numpy as np
from sklearn.metrics import average_precision_score,mean_absolute_error
from common import ROOT

class EvidenceTests(unittest.TestCase):
 def test_revenue_reconciles(self):
  d=json.loads((ROOT/'revenue-retention/results.json').read_text());s=d['summary']
  self.assertAlmostEqual(s['gross_sales']-s['credit_value'],s['net_sales'],places=2)
  self.assertAlmostEqual(sum(r['net_sales'] for r in d['monthly']),s['net_sales'],places=2)
  self.assertEqual(sum(r['customers'] for r in d['segments']),s['known_customers'])
  self.assertTrue(all(0<=r['rate']<=1 for r in d['cohorts']))
 def test_future_values_cannot_change_earlier_forecast_features(self):
  features=runpy.run_path(str(ROOT/'demand-planning/analysis.py'))['features']
  s=pd.Series(np.arange(80,dtype=float),index=pd.date_range('2020-01-01',periods=80))
  original=features(s);altered=s.copy();altered.iloc[50:]=999999
  pd.testing.assert_frame_equal(original.iloc[:51],features(altered).iloc[:51])
  self.assertEqual(original.iloc[40]['lag_1'],39)
  self.assertEqual(original.iloc[40]['mean_7'],36)
 def test_forecast_method_is_selected_on_validation(self):
  d=json.loads((ROOT/'demand-planning/results.json').read_text())
  for p in d['products']:
   expected='Gradient boosting' if p['validation_ml']['mae']<p['validation_baseline']['mae'] else 'Seasonal baseline'
   self.assertEqual(p['method'],expected)
  f=pd.read_csv(ROOT/'demand-planning/backtest.csv')
  self.assertEqual(len(f),150);self.assertEqual(f.date.min(),'2011-11-01');self.assertEqual(f.date.max(),'2011-11-30')
  self.assertAlmostEqual(mean_absolute_error(f.actual,f.selected),d['summary']['selected']['mae'],places=8)
  for p in d['products']:
   r=f[f.sku.astype(str)==p['sku']];col='model' if p['method']=='Gradient boosting' else 'baseline'
   np.testing.assert_allclose(r.selected,r[col])
 def test_conversion_evidence_matches_predictions(self):
  d=json.loads((ROOT/'conversion-intelligence/results.json').read_text());s=d['summary']
  self.assertEqual(s['train_sessions']+s['validation_sessions']+s['test_sessions'],s['raw_sessions'])
  self.assertNotIn('PageValues',d['features']);self.assertNotIn('Revenue',d['features']);self.assertNotIn('Month',d['features'])
  f=pd.read_csv(ROOT/'conversion-intelligence/holdout-predictions.csv')
  self.assertEqual(set(f.month),{'Nov','Dec'});self.assertEqual(len(f),s['test_sessions'])
  self.assertAlmostEqual(average_precision_score(f.actual,f.probability),s['test']['average_precision'],places=10)
  for row in d['thresholds']+[dict(s['locked_result'],threshold=s['locked_threshold'])]:
   pred=f.probability>=row['threshold'];actual=f.actual.eq(1)
   self.assertEqual(int((pred&actual).sum()),row['tp']);self.assertEqual(int((pred&~actual).sum()),row['fp'])
   self.assertEqual(row['tp']+row['fp']+row['fn']+row['tn'],len(f))
 def test_public_dashboard_payload_matches_project_evidence(self):
  all_data=json.loads((ROOT/'portfolio-data.json').read_text())
  for slug,d in all_data.items():self.assertEqual(d,json.loads((ROOT/slug/'results.json').read_text()))
 def test_local_links_exist(self):
  class Links(HTMLParser):
   def __init__(self):super().__init__();self.links=[];self.ids=set()
   def handle_starttag(self,tag,attrs):
    a=dict(attrs)
    if 'id' in a:self.ids.add(a['id'])
    for key in ['href','src']:
     if key in a:self.links.append(a[key])
  for file in ROOT.glob('*.html'):
   parser=Links();parser.feed(file.read_text())
   for href in parser.links:
    url=urlparse(href)
    if url.scheme or href.startswith('//'):continue
    if url.path:self.assertTrue((ROOT/unquote(url.path)).exists(),f'{file.name}: {href}')
    elif url.fragment:self.assertIn(url.fragment,parser.ids)
if __name__=='__main__':unittest.main()
