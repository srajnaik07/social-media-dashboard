import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ----------------------------------------------------
# 1. PAGE CONFIGURATION & ENTERPRISE STYLING
# ----------------------------------------------------
st.set_page_config(
    page_title="PulseMetrics | Social Media Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load FontAwesome 6 via CDN and inject modern clean typography
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Global Font & Header Polishing */
    h1, h2, h3, h4 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Professional Section Badges with External Icons */
    .icon-heading {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .icon-heading i {
        color: #6366f1;
    }

    /* Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #f9fafb;
    }
    .metric-delta {
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 4px;
        color: #10b981;
    }

    /* Clean Chat Message Styling */
    .chat-role-indicator {
        font-weight: 600;
        font-size: 0.85rem;
        color: #6366f1;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. DATA ENGINE
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
            'Filter': platform,
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
# 3. SIDEBAR CONTROLS
# ----------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="icon-heading" style="font-size: 1.25rem;">
            <i class="fa-solid fa-sliders"></i> Control Center
        </div>
    """, unsafe_allow_html=True)
    
    data_source = st.radio("Dataset Mode", ["Enterprise Sample", "Upload External CSV"], label_visibility="collapsed")
    
    df_raw = None
    if data_source == "Upload External CSV":
        uploaded_file = st.file_uploader("Ingest CSV Dataset", type=["csv"])
        if uploaded_file is not None:
            try:
                df_raw = pd.read_csv(uploaded_file)
                if 'Date' in df_raw.columns:
                    df_raw['Date'] = pd.to_datetime(df_raw['Date'])
                st.success("File verified and processed.")
            except Exception as e:
                st.error(f"Ingestion error: {e}")
                df_raw = get_sample_data()
        else:
            df_raw = get_sample_data()
    else:
        df_raw = get_sample_data()

    st.markdown("---")
    st.markdown("""
        <div class="icon-heading" style="font-size: 1rem;">
            <i class="fa-solid fa-filter"></i> Parameters
        </div>
    """, unsafe_allow_html=True)
    
    available_platforms = list(df_raw['Filter'].unique()) if 'Filter' in df_raw.columns else []
    selected_platforms = st.multiselect(
        "Platforms",
        options=available_platforms,
        default=available_platforms
    )
    
    available_types = list(df_raw['Post_Type'].unique()) if 'Post_Type' in df_raw.columns else []
    selected_types = st.multiselect(
        "Content Formats",
        options=available_types,
        default=available_types
    )

# Filter Dataset safely
df = df_raw.copy()
if selected_platforms:
    df = df[df['Filter'].isin(selected_platforms)]
if selected_types and 'Post_Type' in df.columns:
    df = df[df['Post_Type'].isin(selected_types)]

# ----------------------------------------------------
# 4. DASHBOARD HEADER & KPI TILES
# ----------------------------------------------------
st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
            <i class="fa-solid fa-chart-line" style="color: #6366f1;"></i> Social Media Performance Dashboard
        </h1>
        <p style="color: #9ca3af; font-size: 0.95rem; margin: 0;">
            Real-time performance analytics, cross-platform attribution, and exploratory data intelligence.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_impressions = df['Impressions'].sum() if 'Impressions' in df.columns else 0
avg_eng_rate = df['Engagement_Rate'].mean() if 'Engagement_Rate' in df.columns else 0
total_interactions = (df['Likes'].sum() + df['Comments'].sum() + df['Shares'].sum()) if 'Likes' in df.columns else 0
total_posts = len(df)

col1.metric("Total Impressions", f"{total_impressions:,.0f}", "+14.2% MoM")
col2.metric("Avg. Engagement Rate", f"{avg_eng_rate:.2f}%", "+0.8% benchmark")
col3.metric("Total Interactions", f"{total_interactions:,.0f}", "+8.5% MoM")
col4.metric("Indexed Posts", f"{total_posts:,}", f"{len(selected_platforms)} Active Channels")

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. WORKSPACE TABS (CLEAN, NO EMOJIS)
# ----------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Performance Trends", 
    "Platform Attribution", 
    "AI Analytics Assistant", 
    "Dataset Inspector"
])

# ---- TAB 1: PERFORMANCE TRENDS ----
with tab1:
    st.markdown("""
        <div class="icon-heading">
            <i class="fa-solid fa-arrow-trend-up"></i> Cross-Channel Impressions & Growth Trends
        </div>
    """, unsafe_allow_html=True)
    
    if 'Date' in df.columns and not df.empty:
        trend_df = df.groupby(['Date', 'Filter'])['Impressions'].sum().reset_index()
        fig_trend = px.line(
            trend_df, 
            x='Date', 
            y='Impressions', 
            color='Filter',
            template="plotly_dark",
            title="Daily Impression Trajectory by Platform",
            markers=True
        )
        fig_trend.update_layout(hovermode="x unified", height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_trend, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="icon-heading">
                <i class="fa-solid fa-chart-column"></i> Engagement Rate by Format
            </div>
        """, unsafe_allow_html=True)
        if 'Post_Type' in df.columns and 'Engagement_Rate' in df.columns:
            format_df = df.groupby('Post_Type')['Engagement_Rate'].mean().reset_index().sort_values(by='Engagement_Rate', ascending=False)
            fig_format = px.bar(
                format_df, 
                x='Post_Type', 
                y='Engagement_Rate', 
                color='Engagement_Rate',
                color_continuous_scale="Blues",
                template="plotly_dark",
                labels={'Engagement_Rate': 'Avg Engagement (%)', 'Post_Type': 'Content Format'}
            )
            fig_format.update_layout(height=350)
            st.plotly_chart(fig_format, use_container_width=True)

    with c2:
        st.markdown("""
            <div class="icon-heading">
                <i class="fa-solid fa-chart-pie"></i> Interaction Share (Likes, Comments, Shares)
            </div>
        """, unsafe_allow_html=True)
        if all(k in df.columns for k in ['Likes', 'Comments', 'Shares']):
            breakdown_data = pd.DataFrame({
                'Interaction': ['Likes', 'Comments', 'Shares'],
                'Count': [df['Likes'].sum(), df['Comments'].sum(), df['Shares'].sum()]
            })
            fig_pie = px.pie(
                breakdown_data, 
                values='Count', 
                names='Interaction', 
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Prism,
                template="plotly_dark"
            )
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)

# ---- TAB 2: PLATFORM ATTRIBUTION ----
with tab2:
    st.markdown("""
        <div class="icon-heading">
            <i class="fa-solid fa-layer-group"></i> Platform Efficiency & Attribution
        </div>
    """, unsafe_allow_html=True)
    
    if 'Filter' in df.columns:
        p_summary = df.groupby('Filter').agg(
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
                color="Filter",
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
                x="Filter",
                y="Total_Impressions",
                color="Filter",
                template="plotly_dark",
                title="Aggregate Volume by Filter"
            )
            fig_bar_reach.update_layout(height=420)
            st.plotly_chart(fig_bar_reach, use_container_width=True)

# ---- TAB 3: AI ANALYTICS ASSISTANT (CONVERSATIONAL DATA ENGINE) ----
with tab3:
    st.markdown("""
        <div class="icon-heading" style="font-size: 1.15rem;">
            <i class="fa-solid fa-brain"></i> AI Analytics Assistant
        </div>
        <p style="color: #9ca3af; font-size: 0.9rem; margin-bottom: 16px;">
            Deterministic query parsing engine connected to the active filtered dataset.
        </p>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Data engine ready. Sample operational queries:\n- *What is our top performing post?*\n- *Compare platform efficiency*\n- *Provide an executive summary*\n- *What content format drives highest engagement?*"
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    def parse_analytics_query(query: str, current_df: pd.DataFrame) -> str:
        q = query.lower().strip()
        
        if current_df.empty:
            return "Active dataset selection is empty. Adjust platform and format filters in the sidebar."

        # Top Post Intent
        if any(w in q for w in ["highest", "best", "top post", "most popular", "viral", "leading"]):
            best_post = current_df.loc[current_df['Engagement_Rate'].idxmax()]
            return (
                f"**Top Performing Asset Identified:**\n\n"
                f"- **Post ID:** `{best_post.get('Post_ID', 'N/A')}`\n"
                f"- **Channel:** {best_post.get('Filter', 'N/A')}\n"
                f"- **Format:** {best_post.get('Post_Type', 'N/A')}\n"
                f"- **Engagement Rate:** `{best_post.get('Engagement_Rate', 0)}%`\n"
                f"- **Total Reach:** `{best_post.get('Reach', 0):,}`\n"
                f"- **Interactions:** {best_post.get('Likes', 0):,} likes, {best_post.get('Shares', 0):,} shares."
            )

        # Platform Comparison Intent
        elif any(w in q for w in ["platform", "channel", "network", "compare"]):
            best_p = current_df.groupby('Filter')['Engagement_Rate'].mean().idxmax()
            best_p_rate = current_df.groupby('Filter')['Engagement_Rate'].mean().max()
            vol_p = current_df.groupby('Filter')['Impressions'].sum().idxmax()
            vol_num = current_df.groupby('Filter')['Impressions'].sum().max()
            return (
                f"**Cross-Channel Benchmark Analysis:**\n\n"
                f"- **Highest Conversion Efficiency:** **{best_p}** (avg. engagement rate: **{best_p_rate:.2f}%**).\n"
                f"- **Highest Reach Volume:** **{vol_p}** (aggregate impressions: **{vol_num:,}**).\n\n"
                f"*Actionable conclusion: Allocate budget towards {vol_p} for brand awareness, and utilize {best_p} for audience retention.*"
            )

        # Executive Summary Intent
        elif any(w in q for w in ["summary", "overview", "executive", "kpi", "stats", "audit"]):
            return (
                f"**Executive Performance Audit:**\n\n"
                f"- **Indexed Assets:** {len(current_df):,}\n"
                f"- **Gross Impressions:** {current_df['Impressions'].sum():,}\n"
                f"- **Mean Engagement Rate:** {current_df['Engagement_Rate'].mean():.2f}%\n"
                f"- **Total Interactions:** {(current_df['Likes'].sum() + current_df['Comments'].sum() + current_df['Shares'].sum()):,}\n"
                f"- **Leading Asset Type:** {current_df.groupby('Post_Type')['Engagement_Rate'].mean().idxmax()}"
            )

        # Strategic Recommendations Intent
        elif any(w in q for w in ["recommend", "strategy", "improve", "tips", "optimize"]):
            top_format = current_df.groupby('Post_Type')['Engagement_Rate'].mean().idxmax()
            top_channel = current_df.groupby('Filter')['Engagement_Rate'].mean().idxmax()
            return (
                f"**Strategic Distribution Recommendations:**\n\n"
                f"1. **Content Priority:** Increase production volume for **`{top_format}`**, which yields the highest engagement density across data points.\n"
                f"2. **Primary Channel Distribution:** Prioritize organic distribution on **{top_channel}** to maximize interaction-per-impression return.\n"
                f"3. **Audience Retention:** Focus call-to-actions on direct comments to increase algorithmic amplification."
            )

        # Averages & Statistics
        elif any(w in q for w in ["average", "avg", "mean", "metric"]):
            return (
                f"**Dataset Statistical Means:**\n\n"
                f"- Average Impressions / Post: **{current_df['Impressions'].mean():,.0f}**\n"
                f"- Average Engagement Rate: **{current_df['Engagement_Rate'].mean():.2f}%**\n"
                f"- Average Likes / Post: **{current_df['Likes'].mean():,.0f}**\n"
                f"- Average Shares / Post: **{current_df['Shares'].mean():,.0f}**"
            )

        # Context-Aware Fallback
        else:
            return (
                f"**Data Slice Context (`{query}`):**\n\n"
                f"- Scope: **{len(current_df)} filtered posts**\n"
                f"- Leading channel by post count: **{current_df['Filter'].value_counts().index[0]}**\n"
                f"- Segment engagement rate: **{current_df['Engagement_Rate'].mean():.2f}%**\n\n"
                f"Suggested queries:\n"
                f"- *'What is our top performing post?'*\n"
                f"- *'Compare filter efficiency'*\n"
                f"- *'Provide strategic recommendations'*"
            )

    if user_prompt := st.chat_input("Enter analytics query..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        response = parse_analytics_query(user_prompt, df)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# ---- TAB 4: DATASET INSPECTOR ----
with tab4:
    st.markdown("""
        <div class="icon-heading">
            <i class="fa-solid fa-table"></i> Tabular Inspection & Data Export
        </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export Filtered Data (CSV)",
        data=csv_data,
        file_name="social_media_analytics_export.csv",
        mime="text/csv",
    )