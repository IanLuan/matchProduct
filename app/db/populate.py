from database import connection
import pandas as pd
import numpy as np

df = pd.read_csv('../core/data/dataset_final.csv', index_col=0).to_numpy()


def check_null(value):
    if pd.isnull(value):
        return None
    
    return value


def check_null_float(value):
    if pd.isnull(value):
        return None
    elif "," in value:
        return value.replace(",", ".")
    else:
        return value


for index, row in enumerate(df[5978:]):
    query = f"INSERT INTO recommended_products (id, product, brand, unit, number, market) VALUES (%s, %s, %s, %s, %s, %s);"
    connection.execute(query, (index+5978, check_null(row[0]), check_null(row[1]), check_null(row[3]), check_null_float(row[2]), row[4]))
    print("Inserted", index+5978)



query = f'SELECT * FROM recommended_products'
for row in connection.execute(query):
    print(row.product)