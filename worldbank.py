import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Function to fetch data from World Bank API
def fetch_world_bank_data(country_code, indicator_code):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json"
    response = requests.get(url)
    data = response.json()
    if len(data) > 1:
        return data[1][0]['value']
    else:
        return None

# Major countries and their codes (World Bank) - Adding Germany and France back to Eurozone
countries = {
    "United States": "USA",
    "Japan": "JPN",
    "United Kingdom": "GBR",
    "Canada": "CAN",
    "Eurozone": ["DEU", "FRA", "ITA", "ESP", "NLD", "BEL", "AUT", "LUX"]  # Added Germany and France back
}

# Indicators for GDP and other economic data
gdp_indicator = "NY.GDP.MKTP.CD"  # GDP in current USD
inflation_indicator = "FP.CPI.TOTL.ZG"  # Inflation rate
unemployment_indicator = "SL.UEM.TOTL.ZS"  # Unemployment rate
trade_balance_indicator = "NE.EXP.GNFS.ZS"  # Trade Balance (% of GDP)
interest_rate_indicator = "FR.INR.RINR"  # Interest Rate
debt_to_gdp_indicator = "GC.DOD.TOTL.GD.ZS"  # Debt to GDP Ratio
fdi_indicator = "BX.KLT.DINV.WD.GD.ZS"  # Foreign Direct Investment (FDI)

# Function to calculate aggregated data for Eurozone
def get_eurozone_data():
    eurozone_gdp = 0
    eurozone_inflation = 0
    eurozone_unemployment = 0
    eurozone_trade_balance = 0
    eurozone_interest_rate = 0
    eurozone_debt_to_gdp = 0
    eurozone_fdi = 0
    num_countries = len(countries["Eurozone"])

    # Aggregate the data from all Eurozone countries
    for country_code in countries["Eurozone"]:
        eurozone_gdp += fetch_world_bank_data(country_code, gdp_indicator) or 0
        eurozone_inflation += fetch_world_bank_data(country_code, inflation_indicator) or 0
        eurozone_unemployment += fetch_world_bank_data(country_code, unemployment_indicator) or 0
        eurozone_trade_balance += fetch_world_bank_data(country_code, trade_balance_indicator) or 0
        eurozone_interest_rate += fetch_world_bank_data(country_code, interest_rate_indicator) or 0
        eurozone_debt_to_gdp += fetch_world_bank_data(country_code, debt_to_gdp_indicator) or 0
        eurozone_fdi += fetch_world_bank_data(country_code, fdi_indicator) or 0

    # Average the data for Eurozone
    return {
        "Country": "Eurozone",
        "GDP (USD)": eurozone_gdp / num_countries,
        "Inflation Rate (%)": eurozone_inflation / num_countries,
        "Unemployment Rate (%)": eurozone_unemployment / num_countries,
        "Trade Balance (%)": eurozone_trade_balance / num_countries,
        "Interest Rate (%)": eurozone_interest_rate / num_countries,
        "Debt to GDP (%)": eurozone_debt_to_gdp / num_countries,
        "FDI (%)": eurozone_fdi / num_countries
    }

# Create a DataFrame to hold the data
data = []

# Fetch the data for each country (or Eurozone as a group)
for country, code in countries.items():
    if country == "Eurozone":
        # Get aggregated data for Eurozone
        data.append(get_eurozone_data())
    else:
        gdp = fetch_world_bank_data(code, gdp_indicator)
        inflation = fetch_world_bank_data(code, inflation_indicator)
        unemployment = fetch_world_bank_data(code, unemployment_indicator)
        trade_balance = fetch_world_bank_data(code, trade_balance_indicator)
        interest_rate = fetch_world_bank_data(code, interest_rate_indicator)
        debt_to_gdp = fetch_world_bank_data(code, debt_to_gdp_indicator)
        fdi = fetch_world_bank_data(code, fdi_indicator)

        data.append({
            "Country": country,
            "GDP (USD)": gdp,
            "Inflation Rate (%)": inflation,
            "Unemployment Rate (%)": unemployment,
            "Trade Balance (%)": trade_balance,
            "Interest Rate (%)": interest_rate,
            "Debt to GDP (%)": debt_to_gdp,
            "FDI (%)": fdi
        })

df = pd.DataFrame(data)

# Classify the countries into Strong and Weak economies based on new criteria
def classify_economy(row):
    # Classification criteria (simplified)
    if row['GDP (USD)'] > 1e12 and row['Inflation Rate (%)'] < 5 and row['Unemployment Rate (%)'] < 10 and row['Trade Balance (%)'] > 0 and row['Interest Rate (%)'] < 5:
        return "Strong"
    else:
        return "Weak"

df['Economy Type'] = df.apply(classify_economy, axis=1)

# Streamlit UI
st.title("Financial Data Analysis of Major Economies")
st.write("This app retrieves real-time data for the major economies (including Germany and France in the Eurozone) and classifies them into strong and weak economies based on fundamental data.")

# Display the data in a table
st.subheader("Economic Data")
st.dataframe(df)

# Visualizing the data: Pie chart for strong vs weak economies
fig, ax = plt.subplots()
economy_counts = df['Economy Type'].value_counts()
ax.pie(economy_counts, labels=economy_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
st.subheader("Economy Classification")
st.pyplot(fig)

# Visualizing GDP data
fig, ax = plt.subplots()
ax.bar(df['Country'], df['GDP (USD)'], color='skyblue')
ax.set_ylabel("GDP (in USD)")
ax.set_title("GDP of Major Economies")
st.pyplot(fig)

# Visualizing inflation data
fig, ax = plt.subplots()
ax.bar(df['Country'], df['Inflation Rate (%)'], color='orange')
ax.set_ylabel("Inflation Rate (%)")
ax.set_title("Inflation Rate of Major Economies")
st.pyplot(fig)

# Visualizing unemployment data
fig, ax = plt.subplots()
ax.bar(df['Country'], df['Unemployment Rate (%)'], color='green')
ax.set_ylabel("Unemployment Rate (%)")
ax.set_title("Unemployment Rate of Major Economies")
st.pyplot(fig)

# Visualizing trade balance data
fig, ax = plt.subplots()
ax.bar(df['Country'], df['Trade Balance (%)'], color='red')
ax.set_ylabel("Trade Balance (%)")
ax.set_title("Trade Balance of Major Economies")
st.pyplot(fig)

# Visualizing Interest Rates
fig, ax = plt.subplots()
ax.bar(df['Country'], df['Interest Rate (%)'], color='purple')
ax.set_ylabel("Interest Rate (%)")
ax.set_title("Interest Rate of Major Economies")
st.pyplot(fig)

# Visualizing Debt to GDP Ratio
fig, ax = plt.subplots()
ax.bar(df['Country'], df['Debt to GDP (%)'], color='brown')
ax.set_ylabel("Debt to GDP (%)")
ax.set_title("Debt to GDP Ratio of Major Economies")
st.pyplot(fig)

# Visualizing FDI data
fig, ax = plt.subplots()
ax.bar(df['Country'], df['FDI (%)'], color='cyan')
ax.set_ylabel("FDI (%)")
ax.set_title("Foreign Direct Investment of Major Economies")
st.pyplot(fig)
