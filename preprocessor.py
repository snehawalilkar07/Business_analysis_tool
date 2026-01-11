# preprocessor.py
import pandas as pd
import numpy as np

def _normalize_col_name(col):
    return col.strip().lower().replace(' ', '_')

def preprocess_sales(df):
    df = df.copy()
    df.columns = [_normalize_col_name(c) for c in df.columns]

    rename_map = {}
    for c in df.columns:
        if c in ('transaction_id', 'trx_id', 'id'):
            rename_map[c] = 'transaction_id'
        if 'date' in c:
            rename_map[c] = 'date'
        if 'customer' in c:
            rename_map[c] = 'customer_name'
        if 'product' in c:
            rename_map[c] = 'product_name'
        if 'category' in c:
            rename_map[c] = 'product_category'
        if c in ('price', 'price_per_unit', 'unit_price'):
            rename_map[c] = 'price_per_unit'
        if c in ('cost', 'cost_per_unit', 'unit_cost'):
            rename_map[c] = 'cost_per_unit'
        if c in ('quantity', 'qty', 'q'):
            rename_map[c] = 'quantity'

    df = df.rename(columns=rename_map)

    if 'date' not in df.columns:
        raise ValueError("File must contain 'date' column.")
    if 'product_name' not in df.columns:
        raise ValueError("File must contain 'product_name' column.")
    if 'price_per_unit' not in df.columns:
        df['price_per_unit'] = 0
    if 'quantity' not in df.columns:
        df['quantity'] = 1
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(int)
    df['price_per_unit'] = pd.to_numeric(df['price_per_unit'], errors='coerce').fillna(0)
    df['cost_per_unit'] = pd.to_numeric(df.get('cost_per_unit', 0), errors='coerce').fillna(0)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date']).reset_index(drop=True)

    df['total_amount'] = df['price_per_unit'] * df['quantity']
    df['profit_per_unit'] = df['price_per_unit'] - df['cost_per_unit']
    df['total_profit'] = df['profit_per_unit'] * df['quantity']
    df['profit_margin'] = np.where(df['total_amount'] > 0,
                                   (df['total_profit'] / df['total_amount']) * 100, 0)

    return df
