import pandas as pd

df = pd.read_csv("../data/creditcard.csv")

print("Shape:",df.shape)
print("\nColumns:",df.columns.tolist())

print("\nFraud vs Normal")
print(df['Class'].value_counts())
print(f"\nFraud %: {df['Class'].sum()/len(df)*100:.3f}%")
print("\nAmount stats:")
print(df['Amount'].describe())