from .database import connection
import pandas as pd

# Prioridade dos filtros
# 1- Marca + Unidade + Quantidade -> Melhor caso
# 2- Marca -> Mais importante do que unidade e quantidade
# 3- Unidade + Quantidade -> Pode não ter encontrado marca por questão de escrita
# 4- Sem filtro

def filter_products(brand=None, unit=None, number=None):
    result = []
    if brand and unit and number:
        print("prioridade 1")
        query = f'SELECT * FROM recommended_products WHERE LOWER(brand) = LOWER(%s) AND LOWER(unit) = LOWER(%s) AND number = %s'
        result = connection.execute(query, brand, unit, number).fetchall()
    
    if brand and ((not unit or not number) or len(result) == 0):
        print("prioridade 2")
        query = f'SELECT * FROM recommended_products WHERE LOWER(brand) = LOWER(%s)'
        result = connection.execute(query, brand).fetchall()

    if (unit and number) and (not brand or len(result) == 0):
        print("prioridade 3")
        query = f'SELECT * FROM recommended_products WHERE LOWER(unit) = LOWER(%s) AND number = %s'
        result = connection.execute(query, unit, number).fetchall()
   
    if (not brand and not unit and not number) or len(result) == 0:
        print("prioridade 4")
        query = f'SELECT * FROM recommended_products'
        result = connection.execute(query).fetchall()

    return pd.DataFrame(result, columns =['id', 'product', 'brand', 'unit', 'number', 'market'])