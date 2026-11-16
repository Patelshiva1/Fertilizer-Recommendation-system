import pandas as pd
data = pd.read_csv('f2.csv')
# replicate the same normalization
for col in data.select_dtypes(include='object').columns:
    data[col] = data[col].astype(str).str.strip()
data.rename(columns={'Humidity ':'Humidity','Soil Type':'Soil_Type','Crop Type':'Crop_Type','Fertilizer Name':'Fertilizer'}, inplace=True)
print('Object columns after strip:', data.select_dtypes(include=['object']).columns.tolist())
print('Sample value counts for Soil_Type (first 10):')
print(data['Soil_Type'].head(10))

# Encode categorical columns so downstream models get numeric input
from sklearn.preprocessing import LabelEncoder
import pickle

encoders = {}
for col in ['Soil_Type', 'Crop_Type', 'Fertilizer']:
    if col in data.columns:
        if data[col].dtype == 'object' or not pd.api.types.is_numeric_dtype(data[col]):
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col].astype(str))
            encoders[col] = le
            print(f"Encoded column '{col}' — classes: {le.classes_[:10]}{'...' if len(le.classes_)>10 else ''}")
        else:
            print(f"Column '{col}' already numeric — skipping encoding")
    else:
        print(f"Column '{col}' not found — skipping")

# Save fertilizer encoder (used by the web app) if created
if 'Fertilizer' in encoders:
    with open('fertilizer.pkl', 'wb') as fh:
        pickle.dump(encoders['Fertilizer'], fh)
    print("Saved fertilizer encoder to 'fertilizer.pkl'")

# Optionally save cleaned CSV for reuse
data.to_csv('f2_clean.csv', index=False)
print("Saved cleaned dataset to 'f2_clean.csv'")

print('\nFinal dtypes:')
print(data.dtypes)