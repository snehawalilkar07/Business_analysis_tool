# app.py
import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- Page Config -------------------- #
st.set_page_config(page_title="Business Sales Analyzer", layout="wide")
st.title("📊 Business Sales Dashboard")

# -------------------- Sidebar -------------------- #
st.sidebar.title(" Upload Sales File")
uploaded_file = st.sidebar.file_uploader("Upload your sales file (.csv, .xlsx)")

if uploaded_file:
    try:
        filename = uploaded_file.name
        if filename.endswith('.csv'):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file)

        df = preprocessor.preprocess_sales(raw_df)
        st.success("✅ File uploaded and processed successfully!")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        df = None

    if df is not None:

        # -------------------- Filters -------------------- #
        category_list = ["Overall"] + df["product_category"].dropna().unique().tolist()
        selected_category = st.sidebar.selectbox("Filter by Product Category", category_list)

        filtered_df = df if selected_category == "Overall" else df[df["product_category"] == selected_category]

        # -------------------- KPIs -------------------- #
        st.markdown("##  Key Metrics")
        kpis = helper.compute_kpis(filtered_df)
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric(" Total Sales", f"₹{kpis['total_revenue']:,}")
        col2.metric(" Total Profit", f"₹{kpis['total_profit']:,}")
        col3.metric(" Units Sold", kpis['total_units_sold'])
        col4.metric(" Avg Order Value", f"₹{kpis['avg_order_value']:.2f}")
        col5.metric("Profit Margin", f"{kpis['avg_profit_margin']:.2f}%")

        st.divider()

        # -------------------- Monthly Sales Graph -------------------- #
        st.markdown("##  Monthly Sales Timeline")
        monthly_trend = helper.overall_trend(filtered_df)

        if not monthly_trend.empty:
            fig = px.line(
                monthly_trend,
                x="date",
                y="total_amount",
                markers=True,
                title="Monthly Revenue",
                labels={"date": "Month-Year", "total_amount": "Sales (₹)"},
                color_discrete_sequence=["#9C27B0"]   # Purple
            )
            st.plotly_chart(fig, use_container_width=True)

        # -------------------- Daily Sales Graph -------------------- #
        st.markdown("##  Daily Sales Timeline")
        daily_trend = helper.daily_business_trend(filtered_df)

        if not daily_trend.empty:
            fig = px.line(
                daily_trend,
                x="date",
                y="total_amount",
                markers=True,
                title="Daily Sales Activity",
                labels={"date": "Date", "total_amount": "Sales (₹)"},
                color_discrete_sequence=["#FFC0CB"]  # pink
            )
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # -------------------- Weekly Activity -------------------- #
        st.markdown("## Weekly Activity Insights")
        colA, colB = st.columns(2)

        # Most busy day (Sales by weekday)
        filtered_df["weekday"] = filtered_df["date"].dt.day_name()
        weekday_sales = filtered_df.groupby("weekday").total_amount.sum().reset_index()

        with colA:
            st.subheader(" Most Busy Day")
            fig = px.bar(
                weekday_sales,
                x="weekday",
                y="total_amount",
                text="total_amount",
                title="Sales per Day",
                labels={"weekday": "Day of Week", "total_amount": "Sales (₹)"},
                color_discrete_sequence=["#FF9800"]  # Orange
            )
            fig.update_traces(texttemplate="₹%{text:.0f}", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        # Most busy month (Sales by month)
        filtered_df["month"] = filtered_df["date"].dt.strftime("%B")
        month_sales = filtered_df.groupby("month").total_amount.sum().reset_index()

        with colB:
            st.subheader(" Most Busy Month")
            fig = px.bar(
                month_sales,
                x="month",
                y="total_amount",
                text="total_amount",
                title="Sales per Month",
                labels={"month": "Month", "total_amount": "Sales (₹)"},
                color_discrete_sequence=["#2196F3"]  # Blue
            )
            fig.update_traces(texttemplate="₹%{text:.0f}", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # -------------------- Weekly Heatmap -------------------- #
        st.markdown("##  Weekly Sales Heatmap")

        filtered_df["week_num"] = filtered_df["date"].dt.isocalendar().week

        heatmap_data = filtered_df.pivot_table(
            index=filtered_df["weekday"],
            columns="week_num",
            values="total_amount",
            aggfunc="sum"
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))

        sns.heatmap(
            heatmap_data,
            ax=ax,
            cmap="rocket",
            linewidths=0.3,
            linecolor='gray',
            annot=True,
            fmt='.0f',
            cbar_kws={"label": "Sales Amount"},
            square=False
        )

        ax.set_title("Weekly Sales Heatmap", fontsize=18, fontweight='bold', pad=15, color='white')
        ax.set_xlabel("Week Number", fontsize=14, color='white')
        ax.set_ylabel("Day of Week", fontsize=14, color='white')
        plt.xticks(rotation=45, color='white')
        plt.yticks(rotation=0, color='white')

        fig.patch.set_facecolor('#1E1E1E')
        ax.set_facecolor('#1E1E1E')

        st.pyplot(fig)

        # -------------------- Product Analysis -------------------- #
        st.markdown("## Product Analysis")

        required_columns = {"product_name", "price_per_unit", "cost_per_unit", "quantity"}

        if required_columns.issubset(set(filtered_df.columns)):

            filtered_df["Revenue"] = filtered_df["price_per_unit"] * filtered_df["quantity"]
            filtered_df["Profit"] = (filtered_df["price_per_unit"] - filtered_df["cost_per_unit"]) * filtered_df["quantity"]

            product_summary = filtered_df.groupby("product_name").agg(
                Units_Sold=('quantity', 'sum'),
                Total_Revenue=('Revenue', 'sum'),
                Total_Profit=('Profit', 'sum'),
                Avg_Price=('price_per_unit', 'mean'),
                Category=('product_category', lambda x: x.mode()[0] if not x.mode().empty else "Unknown")
            ).reset_index()

            product_summary = product_summary.sort_values(by="Total_Revenue", ascending=False)

            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("### Product Performance")
                st.dataframe(product_summary)
                top_product = product_summary.iloc[0]["product_name"]
                st.success(f" **Best Selling Product: `{top_product}`**")

            with col2:
                fig = px.bar(
                    product_summary.head(10),
                    x="product_name",
                    y="Total_Revenue",
                    text="Total_Revenue",
                    title="Top 10 Products by Revenue",
                    color_discrete_sequence=["#0097A7"]  # Peacock Blue
                )

                fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                fig.update_layout(
                    title_x=0.5,
                    xaxis_title="Product Name",
                    yaxis_title="Revenue",
                    xaxis_tickangle=45,
                    xaxis_tickfont_size=12,
                    legend_title="Category"
                )

                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("⚠️ Missing required columns for product analysis: "
                       + ", ".join(required_columns - set(filtered_df.columns)))
