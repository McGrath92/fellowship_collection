"""
Fellow Collection Dashboard

Purpose: Take fellow's month of fellowship and current collection - output risk group

Inputs:
- Month of fellowship (1-9): numeric
- Current collection: numeric

Output:
- Risk Group: string (On Track, Watch, High Risk, Critical)
"""

# Load needed libraries
import streamlit as st
import pandas as pd

# Percentile data as given by C.M
percentile_data = {
    'Month': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'p_10': [0, 2776.037, 11202.374, 13549.61, 19085.83, 24859.675, 25195.28, 26549.521, 30254.91],
    'p_25': [0, 4978.2075, 13689.055, 18025.34, 23503.0175, 27071.215, 29208.02, 30688.22, 33567.065],
    'p_50': [243.87, 7562.965, 18393.82, 23374.07, 27142.26, 32423.515, 33522.465, 33477.645, 38551.74],
    'p_75': [2049.31, 12953.015, 21512.3275, 27968.61, 32186.3275, 35000.2525, 38845.98, 38924.8375, 45185.775],
    'p_90': [2871.238, 14422.303, 24093.88, 32562.358, 35985.399, 38910.38, 42963.32, 43240.285, 48425.45]
}
percentile_df = pd.DataFrame(percentile_data)

# Risk category mapping
#Update to show cleaner percentiles eventually
risk_cat = {
    'p_0': 'Critical',
    'p_10': 'High Risk',
    'p_25': 'Watch',
    'p_50': 'Watch',
    'p_75': 'On Track',
    'p_90': 'On Track'
}

# Color mapping for visual feedback
risk_colors = {
    'Critical': '🔴',
    'High Risk': '🟠',
    'Watch': '🟡',
    'On Track': '🟢'
}

def find_percentile_column(df, month, current_collection):
    """
    Find the last column where the value is less than current_collection for a given month
    
    Parameters:
    
    month : int
        The month to search for (1-9)
    current_collection : float
        The collection value to compare against
    
    Returns:
    
    str or p_0
        The name of the last column where value <= current_collection, 
        or 'p_0' if none
    """
    # Find the row matching the month
    row = df[df['Month'] == month]
    
    # Check if month exists
    if row.empty:
        return None
    
    # Drop month column
    percentile_cols = [col for col in df.columns if col != 'Month']
    
    # Find the last column where value <= current_collection
    last_col = 'p_0'  # Default to p_0 if value less than any recorded
    for col in percentile_cols:
        if row[col].values[0] <= current_collection:
            last_col = col
        else:
            break  # Stop at first column > current_collection
    
    return last_col

# Streamlit App
st.title("Fellow Collection Dashboard")
st.markdown("---")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    month_input = st.number_input(
        "Fellow Month (1-9)",
        min_value=1,
        max_value=9,
        value=1,
        step=1,
        help="Enter the current month of fellowship (1-9)"
    )

with col2:
    current_collection_input = st.number_input(
        "Current Collection Amount ($)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        format="%.2f",
        help="Enter the fellow's current collection amount"
    )

# Calculate button
if st.button("Calculate Risk Category", type="primary"):
    # Find percentile
    percentile = find_percentile_column(percentile_df, month=month_input, current_collection=current_collection_input)
    
    if percentile is None:
        st.error("Invalid month entered. Please enter a month between 1 and 9.")
    else:
        # Get risk category
        risk_category = risk_cat[percentile]
        risk_symbol = risk_colors[risk_category]
        
        # Display results
        st.markdown("---")
        st.subheader("Results")
        
        # Create columns for results
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.metric("Percentile", percentile.upper())
        
        with res_col2:
            st.metric("Risk Category", f"{risk_symbol} {risk_category}")
        
        # Additional context based on risk level
        if risk_category == "Critical":
            st.error("Fellow is in Critical status. Immediate intervention recommended.")
        elif risk_category == "High Risk":
            st.warning("Fellow is at High Risk. Close monitoring and support needed.")
        elif risk_category == "Watch":
            st.info("Fellow should be monitored. Consider additional support.")
        else:
            st.success("Fellow is On Track. Continue current approach.")

#Display percentile table for reference
with st.expander("View Percentile Reference Table"):
    st.dataframe(percentile_df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Fellow Collection Risk Assessment Tool --- Design In Progress ---")
st.caption("Built by P.M.McGrath")
