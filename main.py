import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Smart Bill Splitter", page_icon="⚡")

st.title("⚡ Smart Bill Splitter (Tapo Edition)")
st.markdown("""
Upload your **Tapo Energy Export** file below. 
This tool will calculate your PC's exact usage for your specific bill dates.
""")

# --- SIDEBAR: BILLING DATES & COSTS ---
st.sidebar.header("1. Bill Settings")
unit_rate = st.sidebar.number_input("Unit Rate (£/kWh)", value=0.28, format="%.4f")
standing_charge_daily = st.sidebar.number_input("Standing Charge (£/day)", value=0.45, format="%.4f")

# Date Selection
st.sidebar.subheader("Billing Period")
# Default to previous month range (e.g., 15th to 14th)
default_start = datetime.now().replace(day=15) 
bill_start_date = st.sidebar.date_input("Start Date", value=default_start)
bill_end_date = st.sidebar.date_input("End Date", value=datetime.now())

st.sidebar.header("2. Flat Usage")
total_kwh_usage = st.sidebar.number_input("Total Flat Usage (from Utility Bill)", value=250.0)

# --- MAIN: FILE UPLOADER ---
st.header("📂 Upload PC Data")
uploaded_file = st.file_uploader("Upload Tapo Export (Excel/CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    try:
        # Load the data depending on file type
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # CLEANUP: Tapo exports can vary. We look for 'time' and 'energy' columns.
        # Usually Tapo exports have columns like "date" and "energy(wh)" or "energy(kwh)"
        # Let's standardize column names for the script
        df.columns = df.columns.str.lower()
        
        # Find the date column
        date_col = next((col for col in df.columns if 'date' in col or 'time' in col), None)
        # Find the energy column (Tapo often exports in Watt-hours 'wh', we need kWh)
        energy_col = next((col for col in df.columns if 'energy' in col), None)

        if date_col and energy_col:
            # Convert date column to datetime objects
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Filter data for the selected date range
            mask = (df[date_col].dt.date >= bill_start_date) & (df[date_col].dt.date <= bill_end_date)
            filtered_data = df.loc[mask]

            # Calculate Total PC Usage in kWh
            # If the column header suggests 'wh', divide by 1000. 
            # Most Tapo exports are in Wh (Watt-hours).
            raw_sum = filtered_data[energy_col].sum()
            
            if "kwh" in energy_col:
                pc_kwh_usage = raw_sum
            else:
                pc_kwh_usage = raw_sum / 1000.0

            st.success(f"✅ Found data! Your PC used **{pc_kwh_usage:.2f} kWh** between {bill_start_date} and {bill_end_date}.")
            
            # --- SHOW THE MATH (The Bill Logic) ---
            bill_days = (bill_end_date - bill_start_date).days + 1
            total_standing_charge = standing_charge_daily * bill_days
            total_energy_cost = total_kwh_usage * unit_rate
            total_bill = total_standing_charge + total_energy_cost
            
            pc_cost = pc_kwh_usage * unit_rate
            shared_cost = total_bill - pc_cost
            
            your_pay = (shared_cost / 2) + pc_cost
            gf_pay = shared_cost / 2
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Bill", f"£{total_bill:.2f}")
            c2.metric("You Pay", f"£{your_pay:.2f}")
            c3.metric("Girlfriend Pays", f"£{gf_pay:.2f}")

            st.caption(f"Calculation: Shared Cost of £{shared_cost:.2f} split 50/50, plus your £{pc_cost:.2f} PC cost.")
            
        else:
            st.error("Could not automatically find 'Date' or 'Energy' columns. Check the file format.")
            st.write("Columns found:", df.columns.tolist())

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("👆 Upload your Tapo export file to see the breakdown.")
