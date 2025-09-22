import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Partner Revenue Projector",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #404040;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stMetric [data-testid="metric-container"] {
        color: #ffffff !important;
        text-align: center;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: bold !important;
        text-align: center;
    }
    .stMetric [data-testid="stMetricDelta"] > div {
        color: #e0e0e0 !important;
        text-align: center;
    }
    .stMetric [data-testid="stMetricLabel"] > div {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-align: center;
    }
    h1 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .accountability-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 30px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .accountability-box h3 {
        color: white !important;
        margin-top: 0;
        margin-bottom: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
    }
    .accountability-tagline {
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 25px;
        font-style: italic;
        opacity: 0.95;
    }
    .accountability-trigger {
        text-align: center;
        font-size: 1rem;
        margin-bottom: 25px;
        font-weight: 500;
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffd700;
    }
    .accountability-list {
        background: rgba(255,255,255,0.08);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
    }
    .accountability-list ul {
        margin: 0;
        padding: 0;
        list-style-type: none;
        display: inline-block;
        text-align: left;
    }
    .accountability-list li {
        margin-bottom: 12px;
        padding-left: 25px;
        position: relative;
        font-size: 1rem;
        line-height: 1.4;
    }
    .accountability-list li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Partner Revenue Projection Dashboard")
st.markdown("### Interactive Revenue Calculator for Partners")


# Sidebar for inputs
with st.sidebar:
    st.header("Parameters")
    st.markdown("---")
    
    # Input fields with better formatting
    st.subheader("User Acquisition")
    monthly_new_users = st.number_input(
        "Monthly New Users",
        min_value=0,
        max_value=10000,
        value=100,
        step=10,
        help="Number of new users acquired each month"
    )
    
    st.subheader("Conversion Settings")
    conversion_rate = st.slider(
        "Conversion Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.5,
        help="Percentage of users who convert to paying customers"
    )
    
    st.subheader("Current Performance")
    current_avg_revenue = st.number_input(
        "Current Avg Revenue per Student ($)",
        min_value=0.0,
        max_value=1000.0,
        value=25.0,
        step=0.5,
        help="Your current average revenue per student for comparison"
    )
    
    st.subheader("Projection Period")
    num_months = st.slider(
        "Number of Months to Project",
        min_value=3,
        max_value=24,
        value=12,
        step=1
    )
    
    st.markdown("---")
    st.info(f"**FireCert Price:** $39")
    
    # Revenue share tiers display
    st.markdown("### 💰 Revenue Share Tiers")
    st.markdown("*Based on converted users*")
    st.success("**Affiliate (0-999):** 30%")
    st.success("**Partner (1,000-1,999):** 60%")
    st.success("**Gold Partner (2,000-2,999):** 65%")
    st.success("**Owner (3,000+):** 70%")
    
    st.markdown("---")
    st.caption("📝 First month conversion is 50% of normal rate (tuning period)")

# Calculate projections
def get_tier_name(converted_users):
    """Get tier name based on converted users"""
    if converted_users < 1000:
        return "Affiliate"
    elif converted_users < 2000:
        return "Partner"
    elif converted_users < 3000:
        return "Gold Partner"
    else:
        return "Owner"

def calculate_revenue_share(converted_users):
    """Calculate revenue share percentage based on converted user tier"""
    if converted_users < 1000:
        return 30
    elif converted_users < 2000:
        return 60
    elif converted_users < 3000:
        return 65
    else:
        return 70

def calculate_projections(monthly_new_users, conversion_rate, num_months):
    """Calculate monthly revenue projections"""
    data = []
    cumulative_users = 0
    cumulative_converted = 0
    cumulative_revenue = 0
    
    for month in range(1, num_months + 1):
        # Add new users
        cumulative_users += monthly_new_users
        
        # Calculate conversion (half rate for first month)
        if month == 1:
            converted_users = monthly_new_users * (conversion_rate / 100) * 0.5
        else:
            converted_users = monthly_new_users * (conversion_rate / 100)
        
        cumulative_converted += converted_users
        
        # Get revenue share percentage based on cumulative converted users
        revenue_share_pct = calculate_revenue_share(cumulative_converted)
        tier_name = get_tier_name(cumulative_converted)
        
        # Calculate revenue
        gross_revenue = converted_users * 39
        partner_revenue = gross_revenue * (revenue_share_pct / 100)
        cumulative_revenue += partner_revenue
        
        data.append({
            'Month': f'Month {month}',
            'Month_Num': month,
            'New Users': monthly_new_users,
            'Cumulative Users': cumulative_users,
            'Converted Users (Monthly)': int(converted_users),
            'Cumulative Converted': int(cumulative_converted),
            'Tier': tier_name,
            'Revenue Share %': revenue_share_pct,
            'Gross Revenue': gross_revenue,
            'Partner Revenue': partner_revenue,
            'Cumulative Revenue': cumulative_revenue,
            '50% Target': cumulative_revenue * 0.5  # NEW: Add 50% threshold
        })
    
    return pd.DataFrame(data)

# Generate projections
df = calculate_projections(monthly_new_users, conversion_rate, num_months)

# Calculate comparison metrics - FIXED CALCULATION
partner_revenue_per_student = 39 * (conversion_rate / 100) * (df['Revenue Share %'].iloc[-1] / 100)
# This is the ADDITIONAL revenue per student, not replacement
additional_revenue_percentage = (partner_revenue_per_student / current_avg_revenue) * 100 if current_avg_revenue > 0 else 0

# Main dashboard area - REMOVED TOTAL USERS METRIC
col1, col2, col3 = st.columns(3)

with col1:
    total_revenue = df['Cumulative Revenue'].iloc[-1]
    st.metric(
        label="Total Partner Revenue",
        value=f"${total_revenue:,.2f}",
        delta=f"Avg ${total_revenue/num_months:,.2f}/month"
    )

with col2:
    final_tier = df['Tier'].iloc[-1]
    final_share = df['Revenue Share %'].iloc[-1]
    st.metric(
        label="Final Tier Status",
        value=f"{final_tier}",
        delta=f"{final_share}% revenue share"
    )

with col3:
    st.metric(
        label="Additional Revenue per Student",
        value=f"${partner_revenue_per_student:.2f}",
        delta=f"+{additional_revenue_percentage:.1f}% additional income"
    )

st.markdown("---")

# Create visualizations - Full width charts
# ENHANCED: Cumulative revenue chart with accountability threshold
fig_revenue = go.Figure()

fig_revenue.add_trace(go.Scatter(
    x=df['Month'],
    y=df['Cumulative Revenue'],
    name='Projected Revenue',
    line=dict(color='darkblue', width=3),
    fill='tozeroy',
    fillcolor='rgba(31,119,180,0.1)',
    text=df['Cumulative Revenue'].apply(lambda x: f'${x:,.0f}'),
    textposition='middle right',
    mode='lines+markers+text'
))

# NEW: Add 50% threshold line with annotation
fig_revenue.add_trace(go.Scatter(
    x=df['Month'],
    y=df['50% Target'],
    name='Investigation Trigger (50%)',
    line=dict(color='orange', width=2, dash='dash'),
    hovertemplate='<b>50% Threshold</b><br>Below this triggers investigation<br>$%{y:,.0f}<extra></extra>'
))

fig_revenue.update_layout(
    title='Cumulative Revenue Growth with Accountability Threshold',
    xaxis_title='Month',
    yaxis_title='Cumulative Revenue ($)',
    hovermode='x unified',
    height=450,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_revenue, use_container_width=True)

# Converted user growth and tier progression
fig_users = go.Figure()

# Add converted user growth line
fig_users.add_trace(go.Scatter(
    x=df['Month'],
    y=df['Cumulative Converted'],
    name='Converted Users',
    line=dict(color='green', width=3),
    fill='tozeroy',
    fillcolor='rgba(0,255,0,0.1)'
))

# Add tier thresholds
for threshold, label in [(1000, 'Partner'), (2000, 'Gold Partner'), (3000, 'Owner')]:
    fig_users.add_hline(
        y=threshold,
        line_dash="dash",
        line_color="red",
        annotation_text=label,
        annotation_position="right"
    )

fig_users.update_layout(
    title='Converted Users & Tier Progression',
    xaxis_title='Month',
    yaxis_title='Cumulative Converted Users',
    height=400,
    showlegend=True
)

st.plotly_chart(fig_users, use_container_width=True)

# Summary insights
st.markdown("---")
st.markdown("""
<div class="accountability-box">
    <h3>Our Accountability Promise</h3>
    <div class="accountability-tagline">
        These aren't just numbers, they're commitments.
    </div>
    <div class="accountability-trigger">
        If performance falls below 50% of projections for 2 consecutive months
    </div>
    <div class="accountability-list">
        <ul>
            <li>10 user interviews conducted at our expense</li>
            <li>Root cause analysis delivered within 14 days</li>
            <li>Custom action plan to get you back on track</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.subheader("Key Insights")

col1, col2 = st.columns(2)

with col1:
    avg_monthly_revenue = df['Partner Revenue'].mean()
    months_to_partner = int(np.ceil(1000 / (monthly_new_users * conversion_rate / 100))) if (monthly_new_users * conversion_rate / 100) > 0 else 'N/A'
    total_converted = df['Cumulative Converted'].iloc[-1]
    
    st.info(f"""
    **Performance Metrics:**
    - Total Converted Users: **{int(total_converted):,}**
    - Average Monthly Revenue: **${avg_monthly_revenue:,.2f}**
    - Months to Partner tier: **{months_to_partner}**
    - Month 1 Revenue (tuning): **${df['Partner Revenue'].iloc[0]:,.2f}**
    - Final Month Revenue: **${df['Partner Revenue'].iloc[-1]:,.2f}**
    """)

with col2:
    if num_months >= 12:
        year_revenue = df['Cumulative Revenue'].iloc[11] if len(df) > 11 else df['Cumulative Revenue'].iloc[-1]
        projected_annual = avg_monthly_revenue * 12
    else:
        year_revenue = df['Cumulative Revenue'].iloc[-1]
        projected_annual = avg_monthly_revenue * 12
    
    total_revenue_per_student = current_avg_revenue + partner_revenue_per_student
    
    st.success(f"""
    **Revenue Comparison:**
    - Current Revenue/Student: **${current_avg_revenue:.2f}**
    - Additional from Partner: **${partner_revenue_per_student:.2f}**
    - Total Revenue/Student: **${total_revenue_per_student:.2f}**
    - Income Increase: **{additional_revenue_percentage:.1f}%**
    - First Year Partner Revenue: **${year_revenue:,.2f}**
    """)


# Footer
st.markdown("---")
st.caption("Adjust parameters in the sidebar to see real-time updates | Performance backed by our Accountability Promise")
