# helper.py
import pandas as pd

def compute_kpis(df):
    df = df.copy()
    for col in ['total_amount', 'total_profit', 'quantity']:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    total_sales = df['total_amount'].sum()
    total_profit = df['total_profit'].sum()
    total_units = df['quantity'].sum()
    avg_order_value = total_sales / len(df) if len(df) > 0 else 0
    avg_profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

    return {
        "total_revenue": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_units_sold": int(total_units),
        "avg_order_value": round(avg_order_value, 2),
        "avg_profit_margin": round(avg_profit_margin, 2)
    }

def overall_trend(df):
    if 'date' not in df.columns:
        return pd.DataFrame()
    temp = df.sort_values('date')
    trend = temp.groupby(temp['date'].dt.to_period('M').astype(str)).agg(
        total_amount=('total_amount', 'sum'),
        total_profit=('total_profit', 'sum')
    ).reset_index().rename(columns={'date':'date'})
    return trend

def daily_business_trend(df):
    if 'date' not in df.columns:
        return pd.DataFrame()
    temp = df.sort_values('date')
    daily = temp.groupby(temp['date'].dt.date).agg(
        total_amount=('total_amount', 'sum'),
        total_profit=('total_profit', 'sum')
    ).reset_index().rename(columns={'date':'date'})
    return daily

def top_products(df, n=10):
    if 'product_name' not in df.columns or 'quantity' not in df.columns:
        return pd.DataFrame()
    return df.groupby('product_name', as_index=False).agg(
        total_quantity=('quantity','sum'),
        total_amount=('total_amount','sum')
    ).sort_values('total_quantity', ascending=False).head(n)

def sales_by_category(df):
    if 'product_category' not in df.columns:
        return pd.DataFrame()
    return df.groupby('product_category', as_index=False).agg(
        total_amount=('total_amount','sum'),
        total_profit=('total_profit','sum')
    ).sort_values('total_amount', ascending=False)

def margin_by_product(df, n=10):
    if not {'product_name','total_amount','total_profit'}.issubset(df.columns):
        return pd.DataFrame()
    temp = df.groupby('product_name', as_index=False).agg(
        total_sales=('total_amount','sum'),
        total_profit=('total_profit','sum')
    )
    temp['profit_margin_%'] = (temp['total_profit']/temp['total_sales'])*100
    return temp.sort_values('profit_margin_%', ascending=False).head(n)
