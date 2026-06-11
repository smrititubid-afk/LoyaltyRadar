# Importing required libraries

import streamlit as st
import pandas as pd
from pathlib import Path

# Setting page configuration
st.set_page_config(
    page_title="LoyaltyRadar Dashboard",
    page_icon="✈️",
    layout="wide"
)

# Creating data path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Loading dashboard data
@st.cache_data
def load_data():
    kpi = pd.read_csv(DATA_DIR / "dashboard_kpi_summary.csv")
    segment = pd.read_csv(DATA_DIR / "dashboard_segment_summary.csv")
    action = pd.read_csv(DATA_DIR / "dashboard_action_summary.csv")
    province = pd.read_csv(DATA_DIR / "dashboard_province_summary.csv")
    roi_kpi = pd.read_csv(DATA_DIR / "dashboard_roi_kpi_summary.csv")
    strategy = pd.read_csv(DATA_DIR / "dashboard_strategy_comparison.csv")
    customers = pd.read_csv(DATA_DIR / "dashboard_customer_table.csv")
    return kpi, segment, action, province, roi_kpi, strategy, customers

kpi, segment, action, province, roi_kpi, strategy, customers = load_data()

# Creating helper function
def get_kpi_value(metric_name):
    return kpi.loc[kpi["metric"] == metric_name, "value"].iloc[0]

# Creating dashboard title
st.title("✈️ LoyaltyRadar")
st.subheader("Recovery-Potential Driven Retention Copilot for Airline Loyalty Teams")

st.write(
    "This prototype helps a non-technical marketing manager identify which loyalty customers need attention, "
    "why they are at risk, and what retention action should be taken next."
)

# Showing KPI cards
st.markdown("## 1. Executive KPI Snapshot")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{int(get_kpi_value('Total Customers')):,}")
col2.metric("Total CLV", f"{get_kpi_value('Total CLV')/1_000_000:.2f}M")
col3.metric("Value at Risk", f"{get_kpi_value('Total Loyalty Value at Risk')/1_000_000:.2f}M")
col4.metric("Value at Risk Share", f"{get_kpi_value('Value at Risk Share (%)'):.1f}%")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Behavioral Churn Customers", f"{int(get_kpi_value('Behavioral Churn Customers')):,}")
col6.metric("Premium Drifters", f"{int(get_kpi_value('Premium Drifters')):,}")
col7.metric("Silent Risk Customers", f"{int(get_kpi_value('Silent Risk Customers')):,}")
col8.metric("Actionable Customers", f"{int(get_kpi_value('Actionable Customers')):,}")

st.info(
    "Interpretation: LoyaltyRadar identifies 2,469 actionable customers and 20.06M loyalty value at risk. "
    "The goal is not to contact everyone, but to prioritize customers with high value and clear actionability."
)

# Creating sidebar filters
st.sidebar.header("Campaign Filters")

segment_filter = st.sidebar.multiselect(
    "Primary segment",
    options=sorted(customers["primary_segment"].dropna().unique()),
    default=sorted(customers["primary_segment"].dropna().unique())
)

action_filter = st.sidebar.multiselect(
    "Next best action",
    options=sorted(customers["next_best_action"].dropna().unique()),
    default=sorted(customers["next_best_action"].dropna().unique())
)

priority_filter = st.sidebar.multiselect(
    "Priority band",
    options=sorted(customers["priority_band"].dropna().unique()),
    default=sorted(customers["priority_band"].dropna().unique())
)

filtered_customers = customers[
    (customers["primary_segment"].isin(segment_filter)) &
    (customers["next_best_action"].isin(action_filter)) &
    (customers["priority_band"].isin(priority_filter))
].copy()

# Showing segment summary
st.markdown("## 2. Segment Summary")

st.write(
    "These segments convert churn and value signals into business-friendly customer groups."
)

st.dataframe(segment, use_container_width=True)

st.bar_chart(
    segment.set_index("primary_segment")["total_value_at_risk"]
)

# Showing action summary
st.markdown("## 3. Next Best Action Summary")

st.write(
    "Each at-risk customer receives a recommended campaign action. Monitor-only customers have no current value at risk."
)

st.dataframe(action, use_container_width=True)

st.bar_chart(
    action.set_index("next_best_action_v2")["total_value_at_risk"]
)

# Showing geography summary
st.markdown("## 4. Regional View")

st.write(
    "This view helps the marketing team identify which provinces contribute the most value at risk."
)

st.dataframe(province, use_container_width=True)

st.bar_chart(
    province.set_index("province")["total_value_at_risk"]
)

# Showing ROI simulation
st.markdown("## 5. Campaign ROI Simulation")

roi_dict = dict(zip(roi_kpi["metric"], roi_kpi["value"]))

r1, r2, r3, r4 = st.columns(4)

r1.metric("Campaign Customers", f"{int(roi_dict['Campaign Customers']):,}")
r2.metric("Total Campaign Cost", f"{roi_dict['Total Campaign Cost']:,.0f}")
r3.metric("Expected Net Value", f"{roi_dict['Expected Net Value']/1_000_000:.2f}M")
r4.metric("Overall ROI Multiple", f"{roi_dict['Overall ROI Multiple']:.2f}x")

st.warning(
    "ROI values are assumption-based simulation estimates, not actual campaign outcomes."
)

st.markdown("### Do Nothing vs Random Targeting vs LoyaltyRadar Targeting")

st.dataframe(strategy, use_container_width=True)

st.bar_chart(
    strategy.set_index("strategy")["expected_net_value"]
)

# Showing customer table
st.markdown("## 6. Campaign-Ready Customer Table")

st.write(
    "This is the final operational table. A marketing manager can filter customers and download the target list."
)

display_columns = [
    "loyalty_number",
    "primary_segment",
    "next_best_action",
    "priority_band",
    "retention_priority_score",
    "recovery_potential_band",
    "recovery_potential_score_v2",
    "clv",
    "loyalty_value_at_risk",
    "clv_tier",
    "loyalty_card",
    "province",
    "city",
    "behavioral_churn",
    "formal_churn"
]

available_display_columns = [
    col for col in display_columns if col in filtered_customers.columns
]

st.dataframe(
    filtered_customers[available_display_columns],
    use_container_width=True,
    height=500
)

st.download_button(
    label="Download filtered campaign list",
    data=filtered_customers.to_csv(index=False),
    file_name="loyaltyradar_filtered_campaign_list.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption(
    "LoyaltyRadar prototype: built for IITG C&A Summer Projects 2026. "
    "The system focuses on behavioral churn, loyalty value at risk, recovery potential, and next-best-action recommendations."
)
