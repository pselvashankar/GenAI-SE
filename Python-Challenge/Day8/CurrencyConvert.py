import streamlit as st
import pandas as pd

# --- Static Exchange Rates ---
# Rates are defined relative to a common base (e.g., 1 unit of USD) 
# for easy cross-conversion. Let's use EUR as the base (Rate of 1.0) 
# for demonstration, but all conversions will be relative to the input currency.
# The rates provided here are purely illustrative and static.
EXCHANGE_RATES = {
    # 1 unit of currency X equals this many units of EUR (our imaginary base)
    "EUR": 1.00,  # Euro (Base currency for static calculations)
    "USD": 0.93,  # US Dollar (1 USD = 0.93 EUR)
    "INR": 0.011, # Indian Rupee (1 INR = 0.011 EUR)
    "GBP": 1.15,  # British Pound (1 GBP = 1.15 EUR) 
    # NOTE: The user asked for "GSP", assuming they meant GBP (Great British Pound).
}

def convert_currency(amount, from_currency, to_currency, rates):
    """
    Converts an amount from one currency to another using the static rates.
    
    The conversion process is:
    1. Convert the 'from_currency' amount to the base currency (EUR).
    2. Convert the base currency amount to the 'to_currency' amount.
    """
    
    # Handle zero or negative amounts gracefully
    if amount is None or amount <= 0:
        return 0.0

    # 1. Convert from_currency to the common base (EUR)
    # 1 / rate[from_currency] = how many EUR per 1 unit of 'from_currency'
    rate_to_base = rates.get(from_currency, 1.0)
    base_amount = amount * rate_to_base
    
    # 2. Convert base (EUR) to the to_currency
    # 1 / rate[to_currency] = how many units of 'to_currency' per 1 EUR
    rate_from_base = 1 / rates.get(to_currency, 1.0)
    
    converted_amount = base_amount * rate_from_base
    return converted_amount

# --- Streamlit UI Layout ---
st.set_page_config(
    page_title="Instant Currency Converter",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("💰 Instant Currency Converter")
st.markdown("Convert between INR, USD, EUR, and GBP using static exchange rates.")

# Define all available currencies for the dropdowns
currency_options = list(EXCHANGE_RATES.keys())

# --- Input Section ---
col1, col2 = st.columns([3, 2])

with col1:
    # Input for the amount
    amount = st.number_input(
        "Enter Amount to Convert", 
        min_value=0.00, 
        value=100.00, 
        step=10.00,
        format="%.2f"
    )

with col2:
    # Dropdown for the source currency
    from_currency = st.selectbox(
        "From Currency",
        currency_options,
        index=currency_options.index("USD") # Default to USD
    )

# st.divider() # Removed for compactness

# --- Results Section ---

# Check if amount is valid before proceeding
if amount > 0:
    # Condensed the header and subheader into a single subheader for less vertical space
    st.subheader(f"Conversion Results for **{from_currency} {amount:,.2f}**")
    
    # Filter the list of currencies to exclude the source currency itself
    target_currencies = [c for c in currency_options if c != from_currency]
    
    # Create a list to hold the conversion results
    results = []
    
    # Perform conversions for all target currencies
    for to_currency in target_currencies:
        converted_value = convert_currency(amount, from_currency, to_currency, EXCHANGE_RATES)
        
        # Store results for display
        results.append({
            "To Currency": to_currency,
            "Rate (1 {} = X {})".format(from_currency, to_currency): 
                convert_currency(1, from_currency, to_currency, EXCHANGE_RATES),
            "Converted Value": f"{to_currency} {converted_value:,.2f}"
        })

    # Display results in a clean DataFrame/table
    results_df = pd.DataFrame(results)
    
    # Apply styling for better readability
    def color_value(val):
        """Custom function to highlight converted value cells."""
        return 'font-weight: bold; background-color: #f0f2f6'

    styled_df = results_df.style.applymap(
        color_value, subset=pd.IndexSlice[:, ['Converted Value']]
    ).format(
        # Format the rate column to show more precision
        {"Rate (1 {} = X {})".format(from_currency, to_currency): "{:,.4f}"}
    )
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

else:
    st.info("Please enter a valid amount greater than zero to see the conversions.")
