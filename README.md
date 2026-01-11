# 📊 Business Sales Analyzer (Streamlit Dashboard)

A **professional, interactive sales analytics dashboard** built using **Streamlit**, designed to help local businesses and analysts understand sales performance, profit trends, and product-level insights from CSV or Excel data.

---

## 🚀 Features

### 🔹 File Upload

* Upload **CSV** or **Excel** sales files
* Automatic data cleaning & preprocessing

### 🔹 Filters

* Filter analysis by **Product Category**

### 🔹 Key Business KPIs

* **Total Sales (Revenue)**
* **Total Profit**
* **Units Sold**
* **Average Order Value**
* **Average Profit Margin**

### 🔹 Sales Trends

* 📈 **Monthly Sales Timeline**
* 📉 **Daily Sales Timeline**

### 🔹 Weekly Insights

* 🗓️ **Most Busy Day of the Week**
* 📆 **Most Busy Month**
* 🔥 **Weekly Sales Heatmap** (Day vs Week)

### 🔹 Product Analysis

* Product-wise:

  * Units Sold
  * Total Revenue
  * Total Profit
  * Average Price
  * Category
* 🏆 Best Selling Product
* 📊 Top 10 Products by Revenue

---

## 🧩 Project Structure

```bash
Business-Sales-Analyzer/
│
├── app.py                 # Main Streamlit app
├── preprocessor.py        # Data cleaning & preprocessing
├── helper.py              # KPI & trend calculation logic
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
└── sample_data/           # (Optional) Sample datasets
```

---

## 📁 Required Dataset Columns

Your sales dataset should include the following columns:

| Column Name      | Description           |
| ---------------- | --------------------- |
| transaction_id   | Unique transaction ID |
| date             | Transaction date      |
| product_name     | Name of product       |
| product_category | Product category      |
| price_per_unit   | Selling price         |
| cost_per_unit    | Cost price            |
| quantity         | Units sold            |

> Column names are automatically normalized (case-insensitive).

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Business-Sales-Analyzer.git
cd Business-Sales-Analyzer
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** – Web UI
* **Pandas & NumPy** – Data processing
* **Plotly Express** – Interactive charts
* **Matplotlib & Seaborn** – Heatmaps & visual styling

---

## 📌 Business Use-Cases

✔ Identify best-selling products
✔ Find peak sales days & months
✔ Track revenue & profit trends
✔ Optimize inventory decisions
✔ Improve pricing & category strategy

---

## 📸 Dashboard Preview

> Add screenshots of your dashboard here for better GitHub presentation.

---

## 🤝 Contribution

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Sujal Songire**
Computer Engineering Student | Python Developer | Data Analyst

---

⭐ If you like this project, don’t forget to **star the repository**!
