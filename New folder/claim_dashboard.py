import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use('Agg')  # Fix for Streamlit Cloud
import matplotlib.pyplot as plt
import os

# Page setup
st.set_page_config(page_title="Claim Quality Dashboard", layout="wide")
st.title("🏥 CLAIM QUALITY ERROR ANALYSIS ENGINE")
st.markdown("---")

# Sidebar for upload
with st.sidebar:
    st.header("📁 Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} claims")
        
        # Show file info
        st.subheader("File Info")
        st.write(f"**Columns:** {len(df.columns)}")
        st.write(f"**Rows:** {len(df)}")
        st.write(f"**Officers:** {df['Officer'].nunique()}")
    else:
        st.info("👆 Please upload a CSV file to begin")
        st.stop()

# Main dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 Errors by Officer")
    officer_counts = df['Officer'].value_counts()
    
    # Pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(officer_counts.values, labels=officer_counts.index, autopct='%1.1f%%')
    ax1.set_title('Error Distribution by Officer')
    st.pyplot(fig1)
    
    # Officer table
    st.write("**Officer Performance:**")
    officer_data = []
    for officer, count in officer_counts.items():
        percentage = (count / len(df)) * 100
        common_error = df[df['Officer'] == officer]['Error_Type'].mode()[0]
        officer_data.append([officer, count, f"{percentage:.1f}%", common_error])
    
    officer_df = pd.DataFrame(officer_data, columns=['Officer', 'Errors', '% Total', 'Most Common Error'])
    st.dataframe(officer_df, use_container_width=True)

with col2:
    st.subheader("🚨 Top Error Types")
    error_counts = df['Error_Type'].value_counts().head(10)
    
    # Bar chart
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    bars = ax2.bar(error_counts.index, error_counts.values, color='#ff6b6b')
    ax2.set_title('Most Frequent Error Types')
    ax2.set_xlabel('Error Type')
    ax2.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)
    
    # Prevention tips
    st.subheader("💡 Prevention Tips")
    tips = {
        "Wrong_Currency": "• Implement auto-currency validation",
        "Data_Entry": "• Add double-check verification step",
        "Missing_Referral": "• Require referral documents before processing",
        "Wrong_Plan": "• Real-time plan verification system",
        "Duplicate_Invoice": "• Invoice duplicate checker",
        "Wrong_Diagnosis": "• Diagnosis-treatment matching tool",
        "Currency_Mismatch": "• Automated currency calculator"
    }
    
    for error in error_counts.head(3).index:
        if error in tips:
            st.info(f"**{error}:** {tips[error]}")

# Bottom section
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.subheader("💰 Financial Impact")
    if 'Payment_Amount' in df.columns:
        total = df['Payment_Amount'].sum()
        avg = df['Payment_Amount'].mean()
        st.metric("Total Payments at Risk", f"${total:,.2f}")
        st.metric("Average per Claim", f"${avg:,.2f}")
    
    # Country analysis
    st.subheader("🌎 Errors by Country")
    if 'Country_of_Treatment' in df.columns:
        country_counts = df['Country_of_Treatment'].value_counts()
        st.dataframe(country_counts)

with col4:
    st.subheader("📊 Quick Stats")
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        st.metric("Total Claims", len(df))
        st.metric("Unique Officers", df['Officer'].nunique())
    
    with stats_col2:
        st.metric("Error Types", df['Error_Type'].nunique())
        if 'Date_of_Invoice' in df.columns:
            df['Date_of_Invoice'] = pd.to_datetime(df['Date_of_Invoice'])
            date_range = f"{df['Date_of_Invoice'].min().date()} to {df['Date_of_Invoice'].max().date()}"
            st.metric("Date Range", date_range)

# Report generation
st.markdown("---")
st.subheader("📄 Generate Reports")

if st.button("📥 Download Summary Report", type="primary"):
    # Create report
    report = []
    report.append("CLAIM QUALITY ANALYSIS REPORT")
    report.append("="*50)
    report.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Claims Analyzed: {len(df)}")
    report.append("\nTOP OFFICERS WITH ERRORS:")
    for officer, count in officer_counts.head(5).items():
        report.append(f"  • {officer}: {count} errors")
    
    report.append("\nRECOMMENDATIONS:")
    for error in error_counts.head(3).index:
        if error in tips:
            report.append(f"  • {error}: {tips[error]}")
    
    # Save and offer download
    report_text = "\n".join(report)
    st.download_button(
        label="⬇️ Download Report (.txt)",
        data=report_text,
        file_name="claim_quality_report.txt",
        mime="text/plain"
    )

st.caption("© Claim Quality Analysis Engine v1.0") 
Fix: Updated for Streamlit Cloud compatibility
