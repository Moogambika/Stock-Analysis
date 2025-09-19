📊 Data-Driven Stock Analysis Dashboard
This repository contains the code for a dynamic stock analysis dashboard built with Streamlit and Python. The application connects to a TiDB database to fetch and display key financial metrics, providing a data-driven overview of the stock market.

The dashboard includes a variety of visualizations to help users understand stock performance, including volatility analysis, cumulative returns, sector-wise performance, and stock correlation.

✨ Features
📈 Volatility Analysis: A bar chart displaying the top 10 most volatile stocks based on the standard deviation of their daily returns.

💹 Cumulative Return Tracker: A line chart that visualizes the cumulative return over time for the top 5 performing stocks.

🏛️ Sector Performance: A bar chart showing the average yearly return for different market sectors, providing a high-level view of industry performance.

🔗 Stock Correlation Heatmap: A heatmap that illustrates the correlation between different stocks, helping to identify relationships and diversification opportunities.

🏆 Monthly Gainers & Losers: A user-selectable view of the top 5 gainers and losers for a specific month, displayed in a clear table format.

🛠️ Technology Stack
Python: The core programming language.

Streamlit: The framework used to create the interactive web application.

Pandas: Essential for data manipulation and analysis.

Plotly Express: Used for generating interactive and visually appealing charts.

SQLAlchemy & PyMySQL: Libraries for connecting to the TiDB database.

TiDB: A MySQL-compatible, scalable database used as the backend data source.

🚀 How to Run the Application
Prerequisites
Python 3.7 or higher.

A running TiDB cluster with the necessary stock data tables.

The required database credentials.

Installation
Clone this repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install the required Python libraries:

Bash

pip install -r requirements.txt
(Note: You'll need to create a requirements.txt file based on the libraries used in app.py. The key libraries are streamlit, pandas, sqlalchemy, plotly_express, pymysql, and urllib.)

Configure your database credentials. Create a .streamlit folder and a secrets.toml file inside it with the following content:

Ini, TOML

[tidb]
user = "your_tidb_username"
password = "your_tidb_password"
host = "your_tidb_host"
port = "your_tidb_port"
database = "your_tidb_database_name"
ssl_ca = "path_to_your_ca_certificate"
This method securely stores your credentials, as required by the st.secrets function in the app.

Running the App
Execute the following command in your terminal:

Bash

streamlit run app.py
The application will open in your default web browser.

📂 Project Structure
.
├── app.py                  # The main Streamlit application script
└── .streamlit/             # Directory for Streamlit configuration
    └── secrets.toml        # Securely stored database credentials
└── README.md               # This file
└── requirements.txt        # List of Python dependencies
