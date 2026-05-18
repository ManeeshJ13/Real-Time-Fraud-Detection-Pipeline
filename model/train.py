import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb
import joblib

df = pd.read_csv('./data/creditcard.csv')
df = df.drop(columns=['Time'])

#scale amount
scaler = RobustScaler()
df['Amount'] = scaler.fit_transform(df[['Amount']])

X = df.drop(columns=['Class'])
y = df['Class']

#startify to ensure ratio
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

#fixing class imbalance
scale_weight = (y_train == 0).sum() / (y_train == 1).sum()
print(f"scale_pos_weight = {scale_weight:.1f}")

model = xgb.XGBClassifier(
    scale_pos_weight = scale_weight,
    n_estimators = 100,
    max_depth = 6,
    learning_rate = 0.1,
    random_state = 42,
    eval_metric = 'auc'
)

model.fit(X_train,y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1]

print("\nClassification Report")
print(classification_report(y_test,y_pred))
print("AUC-ROC:",round(roc_auc_score(y_test,y_pred),4))

joblib.dump(model,'./model/fraud_model.pkl')
joblib.dump(scaler,'./model/scaler.pk1')
print("\nModel + scaler saved")
