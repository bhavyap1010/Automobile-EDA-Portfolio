import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Automobile Market Intelligence Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("data.csv")

    df = df.drop_duplicates()
    df['Market Category'] = df['Market Category'].fillna('Unknown')
    df = df.dropna()
    df = df.drop(df[df['Transmission Type'].str.lower() == 'unknown'].index)
    df.rename(columns={'highway MPG': 'Highway MPG', 'city mpg': 'City MPG', 'Driven_Wheels': 'Driven Wheels'}, inplace=True)
    df = df[(df['Engine Cylinders'] > 0)]
    df = df[(df['MSRP'] >= 1000) & (df['MSRP'] <= 500000)]
    df = df[df['Highway MPG'] >= df['City MPG']]
    df = df[df['Highway MPG'] < 60]
    df['Average MPG'] = (0.6 * df['Highway MPG'] + 0.4 * df['City MPG'])

    df['Price_Segment'] = pd.cut(df['MSRP'],
                                bins=[0, 25000, 50000, 75000, 100000, 500000],
                                labels=['Budget (<$25k)', 'Mid-range ($25k-$50k)',
                                       'Premium ($50k-$75k)', 'Luxury ($75k-$100k)',
                                       'Ultra-luxury (>$100k)'])

    return df

def main():
    st.markdown('<h1 class="main-header">🚗 Automobile Market Intelligence Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")

    df = load_and_clean_data()

    st.sidebar.header("🔍 Filter Options")

    price_range = st.sidebar.slider(
        "Price Range ($)",
        min_value=int(df['MSRP'].min()),
        max_value=int(df['MSRP'].max()),
        value=(int(df['MSRP'].min()), min(100000, int(df['MSRP'].max()))),
        step=5000
    )

    sizes = st.sidebar.multiselect(
        "Vehicle Size",
        options=df['Vehicle Size'].unique(),
        default=df['Vehicle Size'].unique()
    )

    brands = st.sidebar.multiselect(
        "Brands",
        options=sorted(df['Make'].unique()),
        default=sorted(df['Make'].value_counts().head(10).index.tolist())
    )

    filtered_df = df[
        (df['MSRP'] >= price_range[0]) &
        (df['MSRP'] <= price_range[1]) &
        (df['Vehicle Size'].isin(sizes)) &
        (df['Make'].isin(brands))
    ]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="📊 Total Vehicles",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df):,} from full dataset"
        )

    with col2:
        avg_price = filtered_df['MSRP'].mean()
        st.metric(
            label="💰 Average Price",
            value=f"${avg_price:,.0f}",
            delta=f"${avg_price - df['MSRP'].mean():,.0f}"
        )

    with col3:
        avg_mpg = filtered_df['Average MPG'].mean()
        st.metric(
            label="⛽ Average MPG",
            value=f"{avg_mpg:.1f}",
            delta=f"{avg_mpg - df['Average MPG'].mean():.1f}"
        )

    with col4:
        avg_hp = filtered_df['Engine HP'].mean()
        st.metric(
            label="🏎️ Average HP",
            value=f"{avg_hp:.0f}",
            delta=f"{avg_hp - df['Engine HP'].mean():.0f}"
        )

    with col5:
        top_brand = filtered_df['Make'].value_counts().index[0] if len(filtered_df) > 0 else "N/A"
        st.metric(
            label="🏆 Top Brand",
            value=top_brand,
            delta="By volume"
        )

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Price vs Performance Analysis")

        fig_scatter = px.scatter(
            filtered_df,
            x='Engine HP',
            y='MSRP',
            color='Vehicle Size',
            size='Average MPG',
            hover_data=['Make', 'Model', 'Year'],
            title="Price vs Horsepower (Size = MPG, Color = Vehicle Size)",
            labels={'Engine HP': 'Horsepower', 'MSRP': 'Price ($)'}
        )
        fig_scatter.update_layout(height=500)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("🥧 Market Share")

        segment_counts = filtered_df['Price_Segment'].value_counts()
        fig_pie = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="Distribution by Price Segment"
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

        size_counts = filtered_df['Vehicle Size'].value_counts()
        fig_pie2 = px.pie(
            values=size_counts.values,
            names=size_counts.index,
            title="Distribution by Vehicle Size"
        )
        fig_pie2.update_layout(height=300)
        st.plotly_chart(fig_pie2, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⛽ Efficiency Analysis")

        fig_mpg = px.scatter(
            filtered_df,
            x='MSRP',
            y='Average MPG',
            color='Vehicle Size',
            trendline="ols",
            title="Fuel Efficiency vs Price",
            labels={'MSRP': 'Price ($)', 'Average MPG': 'Fuel Efficiency (MPG)'}
        )
        fig_mpg.update_layout(height=400)
        st.plotly_chart(fig_mpg, use_container_width=True)

    with col2:
        st.subheader("🏭 Brand Performance")

        if len(filtered_df) > 0:
            brand_analysis = filtered_df.groupby('Make').agg({
                'MSRP': 'mean',
                'Model': 'count'
            }).round(0).reset_index()
            brand_analysis.columns = ['Brand', 'Avg_Price', 'Model_Count']
            brand_analysis = brand_analysis[brand_analysis['Model_Count'] >= 3].sort_values('Avg_Price', ascending=True)

            fig_brands = px.bar(
                brand_analysis.tail(10),
                x='Avg_Price',
                y='Brand',
                orientation='h',
                title="Average Price by Brand (Min 3 models)",
                labels={'Avg_Price': 'Average Price ($)', 'Brand': 'Brand'}
            )
            fig_brands.update_layout(height=400)
            st.plotly_chart(fig_brands, use_container_width=True)

    st.markdown("---")
    st.subheader("🔍 Market Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**💡 Price-Performance Insight**")
        corr_price_hp = filtered_df['MSRP'].corr(filtered_df['Engine HP'])
        st.write(f"Price-Horsepower correlation: **{corr_price_hp:.3f}**")
        if corr_price_hp > 0.7:
            st.success("Strong positive relationship - Performance drives premium pricing")
        elif corr_price_hp > 0.4:
            st.info("Moderate relationship - Performance influences pricing")
        else:
            st.warning("Weak relationship - Other factors drive pricing")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**⛽ Efficiency Trade-off**")
        corr_price_mpg = filtered_df['MSRP'].corr(filtered_df['Average MPG'])
        st.write(f"Price-MPG correlation: **{corr_price_mpg:.3f}**")
        if corr_price_mpg < -0.4:
            st.info("Clear trade-off: Higher prices = Lower efficiency")
        elif corr_price_mpg > 0.4:
            st.success("Premium efficiency: Higher prices = Better efficiency")
        else:
            st.warning("No clear pattern - Mixed market positioning")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown("**🎯 Market Opportunity**")
        most_popular_size = filtered_df['Vehicle Size'].mode()[0] if len(filtered_df) > 0 else "N/A"
        size_percentage = (filtered_df['Vehicle Size'].value_counts().iloc[0] / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.write(f"Dominant segment: **{most_popular_size}**")
        st.write(f"Market share: **{size_percentage:.1f}%**")
        if size_percentage > 40:
            st.success("Clear market leader - Focus on this segment")
        else:
            st.info("Fragmented market - Multiple opportunities")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Detailed Data View")

    col1, col2, col3 = st.columns(3)
    with col1:
        sort_by = st.selectbox("Sort by:", ['MSRP', 'Average MPG', 'Engine HP', 'Popularity'])
    with col2:
        sort_order = st.radio("Order:", ['Descending', 'Ascending'])
    with col3:
        n_rows = st.number_input("Rows to display:", min_value=10, max_value=100, value=20, step=10)

    ascending = sort_order == 'Ascending'
    display_df = filtered_df.sort_values(sort_by, ascending=ascending).head(n_rows)

    display_columns = ['Make', 'Model', 'Year', 'MSRP', 'Average MPG', 'Engine HP',
                      'Vehicle Size', 'Vehicle Style', 'Transmission Type']

    st.dataframe(
        display_df[display_columns].style.format({
            'MSRP': '${:,.0f}',
            'Average MPG': '{:.1f}',
            'Engine HP': '{:.0f}'
        }),
        use_container_width=True
    )

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"automobile_data_filtered_{len(filtered_df)}_records.csv",
            mime="text/csv"
        )

    with col2:
        st.write(f"**Total Records:** {len(filtered_df):,} / {len(df):,}")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
        "🚗 Automobile Market Intelligence Dashboard | "
        "Data: Car Dataset from Kaggle | "
        "Built with Streamlit & Plotly"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
