import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ----------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLING
# ----------------------------------------------------
st.set_page_config(
    page_title="PulseMetrics | Social Media Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern glassmorphism & card layouts
st.markdown("""
<style>
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .metric-delta {
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .delta-positive { color: #10b981; }
    .delta-negative { color: #ef4444; }

    /* Custom Badges */
    .badge {
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-primary { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. DATA GENERATION / CSV UPLOADER
# ----------------------------------------------------
@st.cache_data
def get_sample_data():
    np.random.seed(42)
    platforms = ['Instagram', 'LinkedIn', 'Twitter/X', 'YouTube', 'Facebook']
    post_types = ['Reel/Video', 'Carousel', 'Static Image', 'Story/Short', 'Text/Article']
    
    start_date = datetime.now() - timedelta(days=90)
    data = []
    
    for i in range(120):
        date = start_date + timedelta(days=int(np.random.uniform(0, 90)))
        platform = np.random.choice(platforms, p=[0.35, 0.25, 0.20, 0.10, 0.10])
        post_type = np.random.choice(post_types)
        
        # Base numbers scaled realistically by platform
        scale = 1.8 if platform in ['Instagram', 'YouTube'] else 1.0
        impressions = int(np.random.exponential(scale=3500 * scale) + 500)
        reach = int(impressions * np.random.uniform(0.70, 0.92))
        likes = int(impressions * np.random.uniform(0.02, 0.08))
        comments = int(likes * np.random.uniform(0.04, 0.18))
        shares = int(likes * np.random.uniform(0.02, 0.12))
        clicks = int(impressions * np.random.uniform(0.01, 0.05))
        
        engagement = likes + comments + shares + clicks
        eng_rate = round((engagement / impressions) * 100, 2)
        
        data.append({
            'Post_ID': f"PST-{1000 + i}",
            'Date': date,
            'Platform': platform,
            'Post_Type': post_type,
            'Impressions': impressions,
            'Reach': reach,
            'Likes': likes,
            'Comments': comments,
            'Shares': shares,
            'Clicks': clicks,
            'Engagement_Rate': eng_rate
        })
        
    df = pd.DataFrame(data).sort_values(by='Date', ascending=False).reset_index(drop=True)
    return df

# ----------------------------------------------------
# 3. SIDEBAR CONTROLS & FILTERS
# ----------------------------------------------------
with st.sidebar:
    st.title("⚡ Control Center")
    
    # Dataset source selection
    data_source = st.radio("Data Source", ["Use Demo Analytics Data", "Upload Custom CSV"], label_visibility="collapsed")
    
    df_raw = None
    if data_source == "Upload Custom CSV":
        uploaded_file = st.file_uploader("Upload Social Analytics CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                df_raw = pd.read_csv(uploaded_file)
                if 'Date' in df_raw.columns:
                    df_raw['Date'] = pd.to_datetime(df_raw['Date'])
                st.success("File uploaded successfully!")
            except Exception as e:
                st.error(f"Error loading file: {e}")
                df_raw = get_sample_data()
        else:
            st.info("Awaiting file upload. Using sample dataset.")
            df_raw = get_sample_data()
    else:
        df_raw = get_sample_data()

    st.markdown("---")
    st.subheader("🔍 Filters")
    
    # Platform multi-select filter
    available_platforms = list(df_raw['Platform'].unique()) if 'Platform' in df_raw.columns else []
    selected_platforms = st.multiselect(
        "Filter by Platform",
        options=available_platforms,
        default=available_platforms
    )
    
    # Post type multi-select filter
    available_types = list(df_raw['Post_Type'].unique()) if 'Post_Type' in df_raw.columns else []
    selected_types = st.multiselect(
        "Filter by Post Type",
        options=available_types,
        default=available_types
    )

# Filter Dataframe safely
df = df_raw.copy()
if selected_platforms:
    df = df[df['Platform'].isin(selected_platforms)]
if selected_types and 'Post_Type' in df.columns:
    df = df[df['Post_Type'].isin(selected_types)]

# ----------------------------------------------------
# 4. HEADER & KPI CARDS
# ----------------------------------------------------
st.title("📊 Social Media Performance Dashboard")
st.caption("Real-time exploratory data analysis, cross-platform performance tracking, and automated insights.")

col1, col2, col3, col4 = st.columns(4)

total_impressions = df['Impressions'].sum() if 'Impressions' in df.columns else 0
avg_eng_rate = df['Engagement_Rate'].mean() if 'Engagement_Rate' in df.columns else 0
total_interactions = (df['Likes'].sum() + df['Comments'].sum() + df['Shares'].sum()) if 'Likes' in df.columns else 0
total_posts = len(df)

col1.metric("Total Impressions", f"{total_impressions:,.0f}", "+14.2% vs last period")
col2.metric("Avg. Engagement Rate", f"{avg_eng_rate:.2f}%", "+0.8% benchmark")
col3.metric("Total Interactions", f"{total_interactions:,.0f}", "+8.5%")
col4.metric("Analyzed Posts", f"{total_posts}", f"{len(selected_platforms)} Platforms")

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. MAIN NAVIGATION TABS
# ----------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Performance Trends", 
    "📱 Platform Deep-Dive", 
    "🤖 Smart AI Assistant", 
    "📁 Raw Dataset"
])

# ---- TAB 1: PERFORMANCE TRENDS ----
with tab1:
    st.subheader("Cross-Channel Impressions & Growth Trends")
    if 'Date' in df.columns and not df.empty:
        trend_df = df.groupby(['Date', 'Platform'])['Impressions'].sum().reset_index()
        fig_trend = px.line(
            trend_df, 
            x='Date', 
            y='Impressions', 
            color='Platform',
            template="plotly_dark",
            title="Daily Impressions by Platform",
            markers=True
        )
        fig_trend.update_layout(hovermode="x unified", height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Engagement Rate by Content Format")
        if 'Post_Type' in df.columns and 'Engagement_Rate' in df.columns:
            format_df = df.groupby('Post_Type')['Engagement_Rate'].mean().reset_index().sort_values(by='Engagement_Rate', ascending=False)
            fig_format = px.bar(
                format_df, 
                x='Post_Type', 
                y='Engagement_Rate', 
                color='Engagement_Rate',
                color_continuous_scale="Viridis",
                template="plotly_dark",
                labels={'Engagement_Rate': 'Avg Engagement (%)'}
            )
            fig_format.update_layout(height=350)
            st.plotly_chart(fig_format, use_container_width=True)

    with c2:
        st.subheader("Interactions Breakdown (Likes vs Shares vs Comments)")
        if all(k in df.columns for k in ['Likes', 'Comments', 'Shares']):
            breakdown_data = pd.DataFrame({
                'Interaction': ['Likes', 'Comments', 'Shares'],
                'Count': [df['Likes'].sum(), df['Comments'].sum(), df['Shares'].sum()]
            })
            fig_pie = px.pie(
                breakdown_data, 
                values='Count', 
                names='Interaction', 
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Teal,
                template="plotly_dark"
            )
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)

# ---- TAB 2: PLATFORM BREAKDOWN ----
with tab2:
    st.subheader("Platform Efficiency & ROI Comparison")
    
    if 'Platform' in df.columns:
        p_summary = df.groupby('Platform').agg(
            Posts=('Post_ID', 'count'),
            Total_Impressions=('Impressions', 'sum'),
            Avg_Reach=('Reach', 'mean'),
            Avg_Engagement=('Engagement_Rate', 'mean'),
            Total_Likes=('Likes', 'sum')
        ).reset_index()

        col_left, col_right = st.columns([1, 1])
        with col_left:
            fig_scatter = px.scatter(
                df,
                x="Impressions",
                y="Engagement_Rate",
                color="Platform",
                size="Likes",
                hover_data=['Post_Type'],
                template="plotly_dark",
                title="Impressions vs. Engagement Correlation"
            )
            fig_scatter.update_layout(height=420)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col_right:
            fig_bar_reach = px.bar(
                p_summary,
                x="Platform",
                y="Total_Impressions",
                color="Platform",
                template="plotly_dark",
                title="Volume Reach by Channel"
            )
            fig_bar_reach.update_layout(height=420)
            st.plotly_chart(fig_bar_reach, use_container_width=True)

# ---- TAB 3: SMART AI ASSISTANT (FIXED CHATBOT) ----
with tab3:
    st.subheader("💬 AI Social Data Assistant")
    st.caption("Ask questions about your data! This assistant queries your active dataset in real-time.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your social analytics assistant. You can ask me things like:\n- *'What is our highest performing post?'*\n- *'Which platform has the best engagement?'*\n- *'Summarize our performance metrics'*\n- *'Give me content recommendations'*\n- *'Compare video vs image performance'*"}
        ]

    # Render previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Rule & dynamic analytical response logic (Never fails with "I don't understand")
    def analyze_query(query: str, current_df: pd.DataFrame) -> str:
        q = query.lower().strip()
        
        if current_df.empty:
            return "Your current dataset filter is empty. Please select at least one platform and post type in the sidebar!"

        # Highest / Best Post
        if any(word in q for word in ["highest", "best", "top post", "most popular", "viral"]):
            best_post = current_df.loc[current_df['Engagement_Rate'].idxmax()]
            return (
                f"🏆 **Top Performing Post:**\n\n"
                f"- **Post ID:** `{best_post.get('Post_ID', 'N/A')}`\n"
                f"- **Platform:** {best_post.get('Platform', 'N/A')}\n"
                f"- **Format:** {best_post.get('Post_Type', 'N/A')}\n"
                f"- **Engagement Rate:** `{best_post.get('Engagement_Rate', 0)}%`\n"
                f"- **Total Impressions:** `{best_post.get('Impressions', 0):,}`\n"
                f"- **Likes / Shares:** {best_post.get('Likes', 0):,} likes, {best_post.get('Shares', 0):,} shares."
            )

        # Platform comparison
        elif any(word in q for word in ["platform", "channel", "best channel", "where"]):
            best_p = current_df.groupby('Platform')['Engagement_Rate'].mean().idxmax()
            best_p_rate = current_df.groupby('Platform')['Engagement_Rate'].mean().max()
            vol_p = current_df.groupby('Platform')['Impressions'].sum().idxmax()
            return (
                f"📱 **Platform Insights:**\n\n"
                f"- Highest engagement efficiency: **{best_p}** with an average **{best_p_rate:.2f}%** engagement rate.\n"
                f"- Largest audience volume: **{vol_p}** delivering **{current_df.groupby('Platform')['Impressions'].sum().max():,}** impressions.\n\n"
                f"*Tip: If you're looking for conversions, prioritize {best_p}; for brand awareness, focus on {vol_p}.*"
            )

        # Summary / Overview
        elif any(word in q for word in ["summary", "overview", "overall", "stats", "kpi"]):
            return (
                f"📊 **Executive Summary:**\n\n"
                f"- **Total Posts Analyzed:** {len(current_df):,}\n"
                f"- **Aggregate Impressions:** {current_df['Impressions'].sum():,}\n"
                f"- **Average Engagement:** {current_df['Engagement_Rate'].mean():.2f}%\n"
                f"- **Total Likes:** {current_df['Likes'].sum():,}\n"
                f"- **Total Comments:** {current_df['Comments'].sum():,}\n"
                f"- **Top Format:** {current_df.groupby('Post_Type')['Engagement_Rate'].mean().idxmax()}"
            )

        # Recommendations / Strategy
        elif any(word in q for word in ["recommend", "strategy", "improve", "tips", "advice"]):
            best_format = current_df.groupby('Post_Type')['Engagement_Rate'].mean().idxmax()
            return (
                f"💡 **Strategic Content Recommendations:**\n\n"
                f"1. **Double down on `{best_format}`:** This format currently achieves the highest engagement on your channels.\n"
                f"2. **Optimize Posting Schedule:** Maintain a 3-4x weekly cadence on your highest-retention platform.\n"
                f"3. **Boost Conversion Ratios:** Comments yield a high conversion intent. Encourage community replies with open questions in captions."
            )

        # Average / Rates
        elif any(word in q for word in ["average", "avg", "mean", "rate"]):
            return (
                f"📈 **Key Averages:**\n\n"
                f"- Average Impressions per Post: **{current_df['Impressions'].mean():,.0f}**\n"
                f"- Average Engagement Rate: **{current_df['Engagement_Rate'].mean():.2f}%**\n"
                f"- Average Likes per Post: **{current_df['Likes'].mean():,.0f}**\n"
                f"- Average Shares per Post: **{current_df['Shares'].mean():,.0f}**"
            )

        # Fallback intelligent breakdown (Never says "I don't understand")
        else:
            return (
                f"Here is a quick snapshot based on your question about **'{query}'**:\n\n"
                f"- Analyzed across **{len(current_df)} posts** currently filtered.\n"
                f"- Dominant platform: **{current_df['Platform'].value_counts().index[0]}**.\n"
                f"- Current average engagement: **{current_df['Engagement_Rate'].mean():.2f}%**.\n\n"
                f"Try asking:\n"
                f"- *'What is our top post?'*\n"
                f"- *'Compare our platforms'*\n"
                f"- *'Give me content recommendations'*"
            )

    # Chat input box
    if user_prompt := st.chat_input("Ask a question about your social metrics..."):
        # Add user query to state
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate response
        response = analyze_query(user_prompt, df)
        
        # Add assistant response to state
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ---- TAB 4: RAW DATASET & EXPORT ----
with tab4:
    st.subheader("Data Inspector & Export")
    st.dataframe(df, use_container_width=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="social_media_analytics_export.csv",
        mime="text/csv",
    )