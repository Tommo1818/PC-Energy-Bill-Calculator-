import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Fair Bill Splitter", page_icon="⚡")

# --- HEADER ---
st.title("⚡ Electricity Bill Splitter")
st.markdown("""
This tool separates your specific **PC usage** from the shared household bill.
Everyone pays 50/50 for the shared electricity and standing charges, 
but you pay 100% of your gaming PC's consumption.
""")

st.markdown("---")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Bill Details")
unit_rate = st.sidebar.number_input(
    "Unit Rate (Price per kWh)", 
    min_value=0.0, 
    value=0.28, 
    format="%.4f",
    help="Check your bill for the unit rate (usually in £ or $)."
)

standing_charge_daily = st.sidebar.number_input(
    "Daily Standing Charge", 
    min_value=0.0, 
    value=0.45, 
    format="%.4f",
    help="The fixed daily cost for electricity connection."
)

bill_days = st.sidebar.number_input(
    "Billing Period (Days)", 
    min_value=1, 
    value=30, 
    step=1
)

st.sidebar.header("2. Usage Data")
total_kwh_usage = st.sidebar.number_input(
    "Total Flat Usage (kWh)", 
    min_value=0.0, 
    value=250.0, 
    step=1.0,
    help="The total kWh used by the entire flat (from your bill)."
)

pc_kwh_usage = st.sidebar.number_input(
    "PC Usage (kWh)", 
    min_value=0.0, 
    value=50.0, 
    step=1.0,
    help="The kWh used by your PC (from your Tapo app)."
)

# --- VALIDATION ---
if pc_kwh_usage > total_kwh_usage:
    st.error("⚠️ Error: PC usage cannot be higher than total flat usage!")
    st.stop()

# --- CALCULATIONS ---
# 1. Costs
total_standing_charge_cost = standing_charge_daily * bill_days
total_energy_cost_bill = total_kwh_usage * unit_rate
calculated_total_bill = total_standing_charge_cost + total_energy_cost_bill

# 2. PC Specifics
pc_cost = pc_kwh_usage * unit_rate

# 3. Shared Specifics
# Shared Energy Cost = Total Energy Cost - PC Cost
# Shared Total = Shared Energy Cost + Standing Charge
shared_energy_cost = total_energy_cost_bill - pc_cost
shared_total_cost = shared_energy_cost + total_standing_charge_cost

# 4. The Split
girlfriend_pay = shared_total_cost / 2
your_pay = (shared_total_cost / 2) + pc_cost

# --- RESULTS DISPLAY ---

# Create columns for the big numbers
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Bill", value=f"£{calculated_total_bill:.2f}")

with col2:
    st.metric(label="You Pay", value=f"£{your_pay:.2f}", delta=f"Includes £{pc_cost:.2f} PC cost")

with col3:
    st.metric(label="Girlfriend Pays", value=f"£{girlfriend_pay:.2f}")

st.markdown("---")

# --- DETAILED BREAKDOWN ---
st.subheader("📊 Detailed Breakdown")

# Create a dataframe for the table
data = {
    "Description": ["Standing Charge", "Shared Electricity", "PC Electricity (Yours)", "TOTAL"],
    "Cost": [
        f"£{total_standing_charge_cost:.2f}",
        f"£{shared_energy_cost:.2f}",
        f"£{pc_cost:.2f}",
        f"**£{calculated_total_bill:.2f}**"
    ],
    "Who Pays?": ["Split 50/50", "Split 50/50", "You (100%)", "-"]
}
df = pd.DataFrame(data)
st.table(df)

# --- VISUALIZATION ---
# Simple bar chart to visualize the split
st.subheader("💸 Payment Split Visualized")
chart_data = pd.DataFrame({
    'Person': ['You', 'Girlfriend'],
    'Amount (£)': [your_pay, girlfriend_pay]
})
st.bar_chart(chart_data.set_index('Person'))

# --- EXPLANATION TEXT ---
st.info(f"""
**Logic Check:**
* The total bill is calculated as **£{calculated_total_bill:.2f}**.
* Your PC cost **£{pc_cost:.2f}** ({pc_kwh_usage} kWh x £{unit_rate:.2f}).
* This is subtracted from the total, leaving **£{shared_total_cost:.2f}** as the 'shared' household cost.
* You both split the shared cost (£{shared_total_cost/2:.2f} each), and you add your PC cost on top.
""")
