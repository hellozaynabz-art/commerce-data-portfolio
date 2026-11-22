"""Month-held-out retrospective conversion classification. No PageValues leakage."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import load_data, dump
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score,roc_auc_score,brier_score_loss,precision_score,recall_score,confusion_matrix
ROOT=Path(__file__).resolve().parent

def metrics(y,p):
 return {'average_precision':float(average_precision_score(y,p)),'roc_auc':float(roc_auc_score(y,p)),'brier':float(brier_score_loss(y,p)),'positive_rate':float(np.mean(y)),'sessions':len(y)}
def threshold_row(y,p,t):
 pred=p>=t;tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
 return {'threshold':round(float(t),2),'precision':float(precision_score(y,pred,zero_division=0)),'recall':float(recall_score(y,pred,zero_division=0)),'flagged':int(pred.sum()),'tp':int(tp),'fp':int(fp),'fn':int(fn),'tn':int(tn)}
def run():
 raw,_=load_data('shoppers');df=raw.copy()
 # UCI says each row represents a distinct user. Identical feature vectors are retained.
 categorical=['OperatingSystems','Browser','Region','TrafficType','VisitorType','Weekend']
 numeric=['Administrative','Administrative_Duration','Informational','Informational_Duration','ProductRelated','ProductRelated_Duration','BounceRates','ExitRates','SpecialDay']
 # Month defines the time split, not an input. PageValues is excluded before fitting.
 columns=numeric+categorical;x=df[columns].copy();y=df.Revenue.astype(int)
 for c in categorical:x[c]=x[c].astype(str)
 train=~df.Month.isin(['Oct','Nov','Dec']);valid=df.Month.eq('Oct');test=df.Month.isin(['Nov','Dec'])
 prep=ColumnTransformer([('num',make_pipeline(SimpleImputer(strategy='median'),StandardScaler()),numeric),('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),categorical)])
 models={'Logistic regression':make_pipeline(prep,LogisticRegression(max_iter=1500,random_state=42)), 'Random forest':make_pipeline(__import__('copy').deepcopy(prep),RandomForestClassifier(n_estimators=250,max_depth=12,min_samples_leaf=8,random_state=42,n_jobs=2))}
 vals={}
 for name,model in models.items():model.fit(x[train],y[train]);vals[name]=metrics(y[valid],model.predict_proba(x[valid])[:,1])
 chosen=max(vals,key=lambda name:vals[name]['average_precision']);model=models[chosen]
 # Fix a 20% review-capacity threshold using validation only, then evaluate unchanged.
 valp=model.predict_proba(x[valid])[:,1];threshold=float(np.quantile(valp,.8))
 model.fit(x[~test],y[~test]);p=model.predict_proba(x[test])[:,1];yt=y[test].values
 measures=metrics(yt,p);fixed=threshold_row(yt,p,threshold)
 baseline=np.repeat(float(y[~test].mean()),len(yt));base=metrics(yt,baseline)
 thresholds=[threshold_row(yt,p,t) for t in np.arange(.05,1,.05)]
 records=pd.DataFrame({'month':df.loc[test,'Month'],'visitor_type':df.loc[test,'VisitorType'],'actual':yt,'probability':p})
 records.to_csv(ROOT/'holdout-predictions.csv',index=False)
 groups=df.groupby(['Month','VisitorType']).agg(sessions=('Revenue','size'),purchases=('Revenue','sum')).reset_index();groups['conversion_rate']=groups.purchases/groups.sessions
 groups.to_csv(ROOT/'session-summary.csv',index=False)
 from sklearn.inspection import permutation_importance
 imp=permutation_importance(model,x[test],y[test],scoring='average_precision',n_repeats=3,random_state=42,n_jobs=2)
 importance=sorted([{'feature':col,'ap_drop':float(v),'std':float(sd)} for col,v,sd in zip(columns,imp.importances_mean,imp.importances_std)],key=lambda r:r['ap_drop'],reverse=True)
 payload={'summary':{'raw_sessions':len(raw),'identical_rows_retained':int(raw.duplicated().sum()),'train_sessions':int(train.sum()),'validation_sessions':int(valid.sum()),'test_sessions':int(test.sum()),'chosen_model':chosen,'test':measures,'baseline':base,'validation':vals,'locked_threshold':threshold,'locked_result':fixed},'thresholds':thresholds,'groups':groups.to_dict('records'),'importance':importance,'features':columns,'excluded':['Revenue (target)','PageValues (potential target leakage)','Month (split variable)']}
 dump(ROOT/'results.json',payload)
 assert not {'PageValues','Revenue','Month'}.intersection(columns)
 assert set(df.loc[train,'Month']).isdisjoint(set(df.loc[test,'Month']))
 assert len(p)==int(test.sum()) and np.isfinite(p).all()
 print('Conversion:',payload['summary'])
 return payload
if __name__=='__main__':run()
