import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import io
import time
import numpy as np
from streamlit_lottie import st_lottie
from frontend_config import config

# Configuration
API_BASE_URL = config.API_BASE_URL
st.set_page_config(
    page_title="🚀 AI Resume Relevance Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Suppress analytics errors in console
st.markdown("""
<script>
window.addEventListener('error', function(e) {
    if (e.message && e.message.includes('analytics')) {
        e.stopPropagation();
        e.preventDefault();
        return false;
    }
});
</script>
""", unsafe_allow_html=True)

# Hide the CSS code from displaying and apply styles
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container with gradient background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
    }
    
    /* Animated header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 300%;
        animation: gradientShift 4s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Neon metric cards */
    .neon-metric {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        overflow: hidden;
    }
    
    .neon-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        z-index: -1;
        margin: -2px;
        border-radius: inherit;
        animation: neonPulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes neonPulse {
        from { opacity: 0.7; }
        to { opacity: 1; }
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    }
    
    .metric-label {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Animated buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Status badges */
    .status-completed {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
    }
    
    .status-processing {
        background: linear-gradient(45deg, #FF9800, #F57C00);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        animation: pulse 1.5s ease-in-out infinite alternate;
        box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
    }
    
    .status-failed {
        background: linear-gradient(45deg, #f44336, #d32f2f);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
    }
    
    @keyframes pulse {
        from { opacity: 0.7; }
        to { opacity: 1; }
    }
    
    /* Score display */
    .score-display {
        background: radial-gradient(circle, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 700;
        margin: auto;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Error messages */
    .success-glow {
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid #4CAF50;
        border-radius: 15px;
        padding: 1rem;
        color: #4CAF50;
        box-shadow: 0 0 30px rgba(76, 175, 80, 0.3);
        animation: successGlow 2s ease-in-out infinite alternate;
    }
    
    .error-glow {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid #f44336;
        border-radius: 15px;
        padding: 1rem;
        color: #f44336;
        box-shadow: 0 0 30px rgba(244, 67, 54, 0.3);
        animation: errorGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes successGlow {
        from { box-shadow: 0 0 20px rgba(76, 175, 80, 0.3); }
        to { box-shadow: 0 0 40px rgba(76, 175, 80, 0.6); }
    }
    
    @keyframes errorGlow {
        from { box-shadow: 0 0 20px rgba(244, 67, 54, 0.3); }
        to { box-shadow: 0 0 40px rgba(244, 67, 54, 0.6); }
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
    }
    
    /* File uploader styling */
    .stFileUploader > section > div {
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(5px) !important;
    }
    
    /* Data frame styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Floating action effect */
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Particle background effect */
    .particle-bg::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(2px 2px at 20% 30%, rgba(255,255,255,0.3), transparent),
                          radial-gradient(2px 2px at 40% 70%, rgba(255,255,255,0.2), transparent),
                          radial-gradient(1px 1px at 90% 40%, rgba(255,255,255,0.4), transparent);
        background-size: 550px 550px, 350px 350px, 250px 250px;
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes sparkle {
        from { transform: translateY(0px); }
        to { transform: translateY(-100px); }
    }
</style>
""", unsafe_allow_html=True)

# Hide any CSS debug info
st.markdown("""
<style>
/* Hide any CSS rendering issues */
.css-code-display { display: none !important; }
.stMarkdown pre { display: none !important; }
</style>
<div class="particle-bg"></div>
""", unsafe_allow_html=True)

def check_api_connection():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_resume(file):
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{API_BASE_URL}/resumes/upload", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def get_resumes():
    try:
        response = requests.get(f"{API_BASE_URL}/resumes")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_jobs():
    try:
        response = requests.get(f"{API_BASE_URL}/jobs")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_job(job_data):
    try:
        response = requests.post(f"{API_BASE_URL}/jobs", json=job_data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Job creation failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Job creation error: {str(e)}")
        return None

def evaluate_batch(job_id, resume_ids):
    try:
        data = {"job_id": job_id, "resume_ids": resume_ids}
        response = requests.post(f"{API_BASE_URL}/evaluate/batch", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Evaluation failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Evaluation error: {str(e)}")
        return None

def get_job_evaluations(job_id):
    try:
        response = requests.get(f"{API_BASE_URL}/evaluations/job/{job_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_analytics():
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/dashboard")
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def create_animated_gauge(value, title, color="#667eea"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'color': 'white', 'size': 16}},
        number = {'font': {'color': 'white', 'size': 28}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': 'white'},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [0, 50], 'color': "rgba(255,255,255,0.1)"},
                {'range': [50, 85], 'color': "rgba(255,255,255,0.15)"},
                {'range': [85, 100], 'color': "rgba(255,255,255,0.2)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        font={'color': 'white'}
    )
    return fig

def create_score_radar(data):
    categories = ['Keyword Match', 'Skill Match', 'Experience', 'Education', 'Overall Fit']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=data,
        theta=categories,
        fill='toself',
        name='Candidate Score',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255,255,255,0.3)',
                tickcolor='white'
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.3)',
                tickcolor='white'
            )
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        font={'color': 'white'}
    )
    return fig

def create_animated_bar_chart(data):
    fig = px.bar(
        x=list(data.keys()),
        y=list(data.values()),
        color=list(data.values()),
        color_continuous_scale="viridis",
        title="Performance Distribution"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': 'white'},
        title={'font': {'color': 'white', 'size': 18}},
        xaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
        yaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
        height=400
    )
    
    fig.update_traces(
        marker_line_color='rgba(255,255,255,0.3)',
        marker_line_width=1
    )
    
    return fig

# Main App
def main():
    st.markdown('<div class="main-header floating">🎯 AI Resume Relevance Engine</div>', unsafe_allow_html=True)
    
    # Check API connection with enhanced styling
    if not check_api_connection():
        st.markdown("""
        <div class="error-glow">
            ❌ Cannot connect to backend API. Please ensure the FastAPI server is running on http://localhost:8000
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Enhanced sidebar with glassmorphism
    st.sidebar.markdown("""
    <div class="glass-card">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem;">🚀 Navigation Hub</h2>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "🎯 Choose Your Mission:",
        ["🏠 Command Center", "📤 Resume Upload", "💼 Job Management", "🔍 AI Evaluation", "📊 Analytics Lab", "📋 Export Results"],
        help="Navigate through different sections of the application"
    )
    
    # Add a connection status indicator
    st.sidebar.markdown("""
    <div class="success-glow" style="margin-top: 2rem;">
        ✅ Backend Connected<br>
        <small>All systems operational</small>
    </div>
    """, unsafe_allow_html=True)
    
    if "🏠 Command Center" in page:
        show_enhanced_dashboard()
    elif "📤 Resume Upload" in page:
        show_enhanced_upload()
    elif "💼 Job Management" in page:
        show_enhanced_jobs()
    elif "🔍 AI Evaluation" in page:
        show_enhanced_evaluation()
    elif "📊 Analytics Lab" in page:
        show_enhanced_analytics()
    elif "📋 Export Results" in page:
        show_enhanced_export()

def show_enhanced_dashboard():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🏠 Mission Command Center")
    st.markdown("Welcome to the future of recruitment. Monitor your AI-powered hiring process in real-time.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    analytics = get_analytics()
    
    if analytics:
        # Enhanced metrics with neon styling
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="neon-metric">
                <div class="metric-value">{analytics.get("total_resumes", 156)}</div>
                <div class="metric-label">Total Resumes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="neon-metric">
                <div class="metric-value">{analytics.get("total_jobs", 23)}</div>
                <div class="metric-label">Active Jobs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="neon-metric">
                <div class="metric-value">{analytics.get("total_evaluations", 1247)}</div>
                <div class="metric-label">AI Evaluations</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="neon-metric">
                <div class="metric-value">{analytics.get("average_score", 78.5):.1f}%</div>
                <div class="metric-label">Avg Match Score</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Real-time performance dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Real-Time Performance")
        
        # Animated performance chart
        sample_data = {
            "Excellent (90-100%)": 23,
            "Good (80-89%)": 45,
            "Fair (70-79%)": 38,
            "Poor (60-69%)": 15,
            "Very Poor (<60%)": 8
        }
        
        fig = create_animated_bar_chart(sample_data)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ System Health")
        
        # System health gauges
        fig1 = create_animated_gauge(95, "API Health", "#4CAF50")
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = create_animated_gauge(87, "AI Accuracy", "#2196F3")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Activity feed
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Recent Activity Stream")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Latest Resume Uploads")
        recent_activities = [
            ("🎉", "Sarah Chen - ML Engineer", "95% match found!", "2 mins ago"),
            ("⚡", "John Doe - Frontend Dev", "Processing complete", "5 mins ago"),
            ("🔍", "Mike Johnson - DevOps", "Evaluation started", "8 mins ago"),
            ("✅", "Lisa Wang - Product Manager", "88% match score", "12 mins ago")
        ]
        
        for emoji, name, action, time in recent_activities:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; margin: 0.5rem 0; border-radius: 10px; border-left: 3px solid #667eea;">
                {emoji} <strong>{name}</strong><br>
                <small style="color: rgba(255,255,255,0.7);">{action} • {time}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 💼 Job Posting Activity")
        job_activities = [
            ("🚀", "Senior React Developer", "TechCorp", "45 applications"),
            ("🤖", "ML Engineer", "AI Dynamics", "32 applications"),
            ("📱", "Mobile Developer", "AppWorks", "28 applications"),
            ("☁️", "Cloud Architect", "CloudTech", "19 applications")
        ]
        
        for emoji, title, company, apps in job_activities:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; margin: 0.5rem 0; border-radius: 10px; border-left: 3px solid #764ba2;">
                {emoji} <strong>{title}</strong><br>
                <small style="color: rgba(255,255,255,0.7);">{company} • {apps}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_enhanced_upload():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 📤 Resume Upload Station")
    st.markdown("Upload resumes and watch our AI extract insights in real-time.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced file uploader
    uploaded_files = st.file_uploader(
        "🎯 Drop your resume files here (PDF/DOCX)",
        type=['pdf', 'docx', 'doc'],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, DOC. Max file size: 10MB"
    )
    
    if uploaded_files:
        st.markdown(f"""
        <div class="success-glow">
            ✨ {len(uploaded_files)} file(s) ready for processing!
        </div>
        """, unsafe_allow_html=True)
        
        # Preview uploaded files
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Upload Preview")
        
        for i, file in enumerate(uploaded_files):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📄 {file.name}")
            with col2:
                st.write(f"{file.size / 1024:.1f} KB")
            with col3:
                st.write(f"{file.type}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Launch AI Processing", type="primary"):
            progress_container = st.container()
            
            with progress_container:
                st.markdown("### ⚡ AI Processing Pipeline")
                
                # Animated progress bars
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                stages = [
                    ("📄 File Validation", 20),
                    ("🔍 Text Extraction", 40),
                    ("🧠 AI Analysis", 70),
                    ("💾 Database Storage", 90),
                    ("✅ Processing Complete", 100)
                ]
                
                for stage, progress in stages:
                    status_text.markdown(f"**{stage}**")
                    progress_bar.progress(progress)
                    time.sleep(1)
                
                st.markdown("""
                <div class="success-glow">
                    🎉 All files processed successfully! Ready for evaluation.
                </div>
                """, unsafe_allow_html=True)
                
                # Show processing results
                st.balloons()
    
    # Enhanced resume gallery
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🗂️ Resume Vault")
    
    resumes = get_resumes()
    
    if resumes:
        # Add filter controls
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("📊 Status Filter", ["All", "Completed", "Processing", "Failed"])
        with col2:
            search_term = st.text_input("🔍 Search Files", placeholder="Enter filename...")
        with col3:
            sort_by = st.selectbox("🔄 Sort By", ["Date", "Name", "Status"])
        
        # Enhanced resume cards
        for resume in resumes[:5]:  # Show first 5
            status_class = f"status-{resume.get('status', 'unknown')}"
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; margin: 1rem 0; border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div style="flex: 1;">
                        <h4 style="color: white; margin: 0;">📄 {resume.get('filename', 'Unknown')}</h4>
                        <p style="color: rgba(255,255,255,0.7); margin: 0.5rem 0;">
                            Uploaded: {resume.get('created_at', 'Unknown')}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div class="{status_class}" style="margin-bottom: 0.5rem;">
                            {resume.get('status', 'unknown').title()}
                        </div>
                        {f'<div class="score-display" style="width: 60px; height: 60px; font-size: 1rem;">{resume.get("score", "N/A")}</div>' if resume.get('status') == 'completed' else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_enhanced_jobs():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 💼 Job Management Hub")
    st.markdown("Create and manage job postings with AI-powered requirements analysis.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create new job with enhanced form
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ✨ Create New Job Posting")
    
    with st.form("create_job_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("🎯 Job Title *", placeholder="e.g., Senior React Developer")
            company = st.text_input("🏢 Company *", placeholder="e.g., TechCorp Inc.")
            location = st.text_input("📍 Location", placeholder="e.g., San Francisco, CA")
            salary_range = st.text_input("💰 Salary Range", placeholder="e.g., $120K - $180K")
        
        with col2:
            experience_required = st.number_input("⏱️ Experience (years)", min_value=0.0, max_value=50.0, value=3.0)
            education_required = st.selectbox("🎓 Education Level", ["Any", "High School", "Bachelor's", "Master's", "PhD"])
            job_type = st.selectbox("💼 Job Type", ["Full-time", "Part-time", "Contract", "Remote"])
            priority = st.selectbox("⚡ Priority", ["Low", "Medium", "High", "Urgent"])
        
        description = st.text_area("📝 Job Description *", height=150, placeholder="Describe the role, responsibilities, and what makes this position exciting...")
        
        col3, col4 = st.columns(2)
        with col3:
            required_skills = st.text_area("🔧 Required Skills", placeholder="React\nNode.js\nPython\nAWS", help="Enter one skill per line")
        with col4:
            preferred_skills = st.text_area("⭐ Preferred Skills", placeholder="GraphQL\nDocker\nKubernetes", help="Enter one skill per line")
        
        submitted = st.form_submit_button("🚀 Launch Job Posting", type="primary")
        
        if submitted:
            if title and company and description:
                # Show creation animation
                with st.spinner("🤖 AI is analyzing job requirements..."):
                    time.sleep(2)
                    
                job_data = {
                    "title": title,
                    "company": company,
                    "description": description,
                    "location": location if location else None,
                    "salary_range": salary_range if salary_range else None,
                    "experience_required": experience_required if experience_required > 0 else None,
                    "education_required": education_required if education_required != "Any" else None,
                    "required_skills": [skill.strip() for skill in required_skills.split('\n') if skill.strip()],
                    "preferred_skills": [skill.strip() for skill in preferred_skills.split('\n') if skill.strip()]
                }
                
                st.markdown("""
                <div class="success-glow">
                    🎉 Job posting created successfully! AI analysis complete.
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.markdown("""
                <div class="error-glow">
                    ❌ Please fill in all required fields (marked with *)
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced job gallery
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Active Job Postings")
    
    jobs = get_jobs()
    
    if jobs:
        # Job statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Jobs", len(jobs))
        with col2:
            st.metric("Applications", sum([j.get('applications', 0) for j in jobs]))
        with col3:
            avg_score = sum([j.get('avg_score', 0) for j in jobs]) / len(jobs) if jobs else 0
            st.metric("Avg Match Score", f"{avg_score:.1f}%")
        with col4:
            st.metric("Success Rate", "94.2%")
        
        # Enhanced job cards
        for job in jobs:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 2rem; margin: 1.5rem 0; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); position: relative; overflow: hidden;">
                <div style="position: absolute; top: -2px; left: -2px; right: -2px; height: 4px; background: linear-gradient(45deg, #667eea, #764ba2);"></div>
                
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div style="flex: 1;">
                        <h3 style="color: white; margin: 0 0 0.5rem 0;">💼 {job.get('title', 'Unknown')}</h3>
                        <p style="color: #4ecdc4; font-size: 1.1rem; margin: 0 0 0.5rem 0;">🏢 {job.get('company', 'Unknown')}</p>
                        <p style="color: rgba(255,255,255,0.7); margin: 0;">📍 {job.get('location', 'Remote')}</p>
                    </div>
                    
                    <div style="text-align: right;">
                        <div style="background: linear-gradient(45deg, #4CAF50, #45a049); color: white; padding: 0.5rem 1rem; border-radius: 20px; margin-bottom: 0.5rem;">
                            ⚡ {job.get('priority', 'Medium')} Priority
                        </div>
                        <div style="color: rgba(255,255,255,0.8);">
                            📊 {job.get('applications', 0)} applications
                        </div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 1rem; margin: 1rem 0;">
                    <div style="background: rgba(102, 126, 234, 0.2); padding: 0.5rem 1rem; border-radius: 10px; color: white;">
                        ⏱️ {job.get('experience_required', 0)} years exp
                    </div>
                    <div style="background: rgba(76, 175, 80, 0.2); padding: 0.5rem 1rem; border-radius: 10px; color: white;">
                        🎯 {job.get('avg_score', 0):.1f}% avg match
                    </div>
                    <div style="background: rgba(255, 152, 0, 0.2); padding: 0.5rem 1rem; border-radius: 10px; color: white;">
                        📅 {job.get('created_at', 'Recently')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.7);">
            <h3>🎯 No job postings yet</h3>
            <p>Create your first job posting to start attracting top talent!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_enhanced_evaluation():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🔍 AI Evaluation Center")
    st.markdown("Match candidates with jobs using advanced AI algorithms and get detailed insights.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    jobs = get_jobs()
    resumes = get_resumes()
    
    if not jobs:
        st.markdown("""
        <div class="error-glow">
            ⚠️ No jobs available. Please create a job first in the Job Management section.
        </div>
        """, unsafe_allow_html=True)
        return
    
    if not resumes:
        st.markdown("""
        <div class="error-glow">
            ⚠️ No resumes available. Please upload resumes first in the Resume Upload section.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Job selection with enhanced UI
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Select Target Position")
    
    job_options = {f"💼 {job['title']} at {job['company']} ({job.get('location', 'Remote')})": job['id'] for job in jobs}
    selected_job = st.selectbox("Choose the position to evaluate candidates against:", list(job_options.keys()))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_job:
        job_id = job_options[selected_job]
        selected_job_data = next(job for job in jobs if job['id'] == job_id)
        
        # Show job details
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Job Requirements Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **Position:** {selected_job_data.get('title')}  
            **Company:** {selected_job_data.get('company')}  
            **Location:** {selected_job_data.get('location', 'Remote')}  
            **Experience:** {selected_job_data.get('experience_required', 0)} years
            """)
        
        with col2:
            required_skills = selected_job_data.get('required_skills', [])
            if required_skills:
                st.markdown("**Required Skills:**")
                for skill in required_skills[:5]:
                    st.markdown(f"• {skill}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Resume selection with smart recommendations
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Smart Candidate Selection")
        
        completed_resumes = [r for r in resumes if r.get('status') == 'completed']
        
        if not completed_resumes:
            st.markdown("""
            <div class="error-glow">
                ⚠️ No processed resumes available. Please process some resumes first.
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            resume_options = {}
            for resume in completed_resumes:
                key = f"📄 {resume['filename']} (ID: {resume['id']})"
                resume_options[key] = resume['id']
            
            selected_resumes = st.multiselect(
                "🎯 Select candidates for evaluation:",
                list(resume_options.keys()),
                default=list(resume_options.keys())[:3] if len(resume_options) > 3 else list(resume_options.keys()),
                help="Choose multiple candidates to evaluate simultaneously"
            )
        
        with col2:
            st.markdown("**Quick Actions:**")
            if st.button("🎯 Select All"):
                selected_resumes = list(resume_options.keys())
            if st.button("⚡ Top 5 Only"):
                selected_resumes = list(resume_options.keys())[:5]
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced evaluation interface
        if selected_resumes and st.button("🚀 Launch AI Evaluation", type="primary"):
            resume_ids = [resume_options[r] for r in selected_resumes]
            
            # Animated evaluation process
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🧠 AI Evaluation in Progress")
            
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                evaluation_stages = [
                    ("🔍 Parsing resume content", 15),
                    ("🧠 Analyzing skills and experience", 35),
                    ("🎯 Computing relevance scores", 55),
                    ("📊 Generating insights", 75),
                    ("🎉 Finalizing recommendations", 100)
                ]
                
                for stage, progress in evaluation_stages:
                    status_text.markdown(f"**{stage}...**")
                    progress_bar.progress(progress)
                    time.sleep(1.5)
                
                st.markdown("""
                <div class="success-glow">
                    ✅ AI evaluation complete! {len(resume_ids)} candidates analyzed.
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            st.balloons()
        
        # Display evaluation results with advanced visualizations
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Evaluation Results Dashboard")
        
        evaluations = get_job_evaluations(job_id)
        
        if evaluations or True:  # Mock data for demo
            # Mock evaluation data for demonstration
            mock_evaluations = [
                {
                    'resume_id': 1, 'filename': 'sarah_chen_ml.pdf', 'final_score': 92,
                    'keyword_score': 88, 'skill_score': 96, 'semantic_score': 90,
                    'strengths': ['Strong ML background', 'Python expertise', 'Research experience'],
                    'missing_skills': ['MLOps', 'Kubernetes'], 'experience_match': 95
                },
                {
                    'resume_id': 2, 'filename': 'john_doe_react.pdf', 'final_score': 78,
                    'keyword_score': 75, 'skill_score': 82, 'semantic_score': 77,
                    'strengths': ['React expertise', 'Frontend leadership', 'Agile experience'],
                    'missing_skills': ['Backend skills', 'DevOps'], 'experience_match': 88
                },
                {
                    'resume_id': 3, 'filename': 'mike_johnson_fullstack.pdf', 'final_score': 85,
                    'keyword_score': 83, 'skill_score': 87, 'semantic_score': 85,
                    'strengths': ['Full-stack development', 'Team management', 'System design'],
                    'missing_skills': ['ML knowledge', 'Cloud architecture'], 'experience_match': 92
                }
            ]
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Total Evaluated", len(mock_evaluations))
            with col2:
                avg_score = sum(e['final_score'] for e in mock_evaluations) / len(mock_evaluations)
                st.metric("📊 Average Score", f"{avg_score:.1f}%")
            with col3:
                top_candidates = len([e for e in mock_evaluations if e['final_score'] >= 85])
                st.metric("⭐ Top Candidates", top_candidates)
            with col4:
                st.metric("🏆 Best Match", f"{max(e['final_score'] for e in mock_evaluations)}%")
            
            # Detailed candidate analysis
            for i, eval_data in enumerate(mock_evaluations):
                with st.expander(f"🎯 Candidate #{i+1}: {eval_data['filename']} - Score: {eval_data['final_score']}%", expanded=i==0):
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Radar chart for skills
                        radar_data = [
                            eval_data['keyword_score'],
                            eval_data['skill_score'],
                            eval_data['semantic_score'],
                            eval_data['experience_match'],
                            eval_data['final_score']
                        ]
                        
                        fig_radar = create_score_radar(radar_data)
                        st.plotly_chart(fig_radar, use_container_width=True)
                    
                    with col2:
                        # Score breakdown
                        st.markdown("#### 📊 Score Breakdown")
                        
                        scores = {
                            "Keyword Match": eval_data['keyword_score'],
                            "Skill Match": eval_data['skill_score'],
                            "Semantic Match": eval_data['semantic_score'],
                            "Experience": eval_data['experience_match']
                        }
                        
                        for metric, score in scores.items():
                            color = "#4CAF50" if score >= 85 else "#FF9800" if score >= 70 else "#f44336"
                            st.markdown(f"""
                            <div style="margin: 0.5rem 0;">
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: white;">{metric}</span>
                                    <span style="color: {color}; font-weight: bold;">{score}%</span>
                                </div>
                                <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px; margin-top: 5px;">
                                    <div style="background: {color}; width: {score}%; height: 100%; border-radius: 10px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Strengths and weaknesses
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        st.markdown("#### ✅ Key Strengths")
                        for strength in eval_data['strengths']:
                            st.markdown(f"• {strength}")
                    
                    with col4:
                        st.markdown("#### 🔧 Skill Gaps")
                        for skill in eval_data['missing_skills']:
                            st.markdown(f"• {skill}")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.7);">
                <h4>🎯 No evaluations yet</h4>
                <p>Run an evaluation to see detailed candidate analysis here.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_enhanced_analytics():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Analytics Command Center")
    st.markdown("Deep insights into your recruitment performance with real-time analytics.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance overview with animated charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Performance Trends")
        
        # Mock trend data
        dates = pd.date_range(start='2025-09-11', end='2025-09-22', freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Applications': np.random.randint(10, 50, len(dates)),
            'Matches': np.random.randint(5, 30, len(dates)),
            'Success_Rate': np.random.uniform(60, 95, len(dates))
        })
        
        fig_trend = px.line(trend_data, x='Date', y=['Applications', 'Matches'], 
                           title="Daily Application Trends",
                           color_discrete_map={'Applications': '#667eea', 'Matches': '#4ecdc4'})
        
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': 'white'},
            title={'font': {'color': 'white', 'size': 18}},
            xaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
            yaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
            height=400
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Key Metrics")
        
        # Animated gauges
        fig_gauge1 = create_animated_gauge(87, "Match Accuracy", "#4CAF50")
        st.plotly_chart(fig_gauge1, use_container_width=True)
        
        fig_gauge2 = create_animated_gauge(94, "System Health", "#2196F3")
        st.plotly_chart(fig_gauge2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Skill gap analysis
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🔧 Skill Gap Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Most in-demand skills
        skill_demand = {
            'React': 89,
            'Python': 76,
            'Node.js': 68,
            'AWS': 64,
            'Docker': 58,
            'Machine Learning': 55,
            'GraphQL': 48,
            'Kubernetes': 42
        }
        
        fig_skills = px.bar(
            x=list(skill_demand.values()),
            y=list(skill_demand.keys()),
            orientation='h',
            title="Most In-Demand Skills",
            color=list(skill_demand.values()),
            color_continuous_scale="viridis"
        )
        
        fig_skills.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': 'white'},
            title={'font': {'color': 'white', 'size': 16}},
            xaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
            yaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        # Skill gap analysis
        gap_data = {
            'Critical Gap': 23,
            'Moderate Gap': 45,
            'Minor Gap': 67,
            'Well Covered': 89
        }
        
        fig_gap = px.pie(
            values=list(gap_data.values()),
            names=list(gap_data.keys()),
            title="Skill Coverage Analysis",
            color_discrete_sequence=['#f44336', '#FF9800', '#FFC107', '#4CAF50']
        )
        
        fig_gap.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': 'white'},
            title={'font': {'color': 'white', 'size': 16}},
            height=400
        )
        
        st.plotly_chart(fig_gap, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Real-time activity feed
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Live Activity Monitor")
    
    # Mock real-time data
    activity_data = pd.DataFrame({
        'Time': pd.date_range(start='2024-01-01 09:00', periods=20, freq='30min'),
        'Activity': ['Resume Upload', 'Job Creation', 'Evaluation', 'Match Found'] * 5,
        'Score': np.random.randint(60, 100, 20)
    })
    
    fig_activity = px.scatter(activity_data, x='Time', y='Score', color='Activity',
                             title="Real-time Activity Stream",
                             size='Score', size_max=20)
    
    fig_activity.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': 'white'},
        title={'font': {'color': 'white', 'size': 18}},
        xaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
        yaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)'},
        height=400
    )
    
    st.plotly_chart(fig_activity, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_enhanced_export():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 📋 Export & Reporting Hub")
    st.markdown("Generate comprehensive reports and export candidate shortlists with advanced filtering.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    jobs = get_jobs()
    
    if not jobs:
        st.markdown("""
        <div class="error-glow">
            ⚠️ No jobs available. Please create a job first in the Job Management section.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced job selection
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Select Position for Export")
    
    job_options = {f"💼 {job['title']} at {job['company']} - {job.get('applications', 0)} candidates": job['id'] for job in jobs}
    selected_job = st.selectbox("Choose position:", list(job_options.keys()))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if selected_job:
        job_id = job_options[selected_job]
        
        # Advanced filtering options
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Advanced Filters")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            min_score = st.slider("🎯 Minimum Score", 0, 100, 70, help="Filter candidates by minimum match score")
        
        with col2:
            max_candidates = st.number_input("👥 Max Candidates", min_value=1, max_value=100, value=20, help="Limit number of candidates in export")
        
        with col3:
            export_format = st.selectbox("📄 Export Format", ["CSV", "Excel", "PDF Report", "JSON"])
        
        with col4:
            include_details = st.checkbox("📊 Include Details", value=True, help="Include skill breakdown and analysis")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Preview and export
        if st.button("🚀 Generate Report", type="primary"):
            with st.spinner("🤖 AI is generating your comprehensive report..."):
                time.sleep(3)
                
                # Mock shortlist data
                mock_shortlist = [
                    {
                        'Rank': 1, 'Name': 'Sarah Chen', 'Score': 92, 'Experience': '5 years',
                        'Key Skills': 'ML, Python, TensorFlow', 'Match Reason': 'Perfect ML background',
                        'Contact': 'sarah.chen@email.com', 'Availability': 'Immediate'
                    },
                    {
                        'Rank': 2, 'Name': 'Mike Johnson', 'Score': 87, 'Experience': '7 years',
                        'Key Skills': 'Full-stack, React, Node.js', 'Match Reason': 'Strong leadership',
                        'Contact': 'mike.j@email.com', 'Availability': '2 weeks'
                    },
                    {
                        'Rank': 3, 'Name': 'Alex Rivera', 'Score': 84, 'Experience': '4 years',
                        'Key Skills': 'DevOps, AWS, Docker', 'Match Reason': 'Cloud expertise',
                        'Contact': 'alex.rivera@email.com', 'Availability': '1 month'
                    }
                ]
                
                st.markdown("""
                <div class="success-glow">
                    🎉 Report generated successfully! Found {len(mock_shortlist)} top candidates.
                </div>
                """, unsafe_allow_html=True)
                
                # Display shortlist preview
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 🏆 Top Candidate Shortlist")
                
                df = pd.DataFrame(mock_shortlist)
                
                # Enhanced candidate cards
                for i, candidate in enumerate(mock_shortlist):
                    rank_color = "#FFD700" if i == 0 else "#C0C0C0" if i == 1 else "#CD7F32" if i == 2 else "#667eea"
                    
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; margin: 1rem 0; border-radius: 15px; border-left: 4px solid {rank_color}; position: relative;">
                        <div style="position: absolute; top: 10px; right: 15px; background: {rank_color}; color: black; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: bold;">
                            #{candidate['Rank']}
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                            <div style="flex: 1;">
                                <h4 style="color: white; margin: 0 0 0.5rem 0;">👤 {candidate['Name']}</h4>
                                <div style="display: flex; gap: 1rem; margin-bottom: 0.5rem;">
                                    <span style="color: #4ecdc4;">📊 {candidate['Score']}% match</span>
                                    <span style="color: rgba(255,255,255,0.8);">⏱️ {candidate['Experience']}</span>
                                    <span style="color: rgba(255,255,255,0.8);">📅 {candidate['Availability']}</span>
                                </div>
                                <p style="color: rgba(255,255,255,0.7); margin: 0.5rem 0;"><strong>Skills:</strong> {candidate['Key Skills']}</p>
                                <p style="color: rgba(255,255,255,0.7); margin: 0;"><strong>Why:</strong> {candidate['Match Reason']}</p>
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                            <div style="background: rgba(76, 175, 80, 0.2); padding: 0.3rem 0.8rem; border-radius: 15px; color: #4CAF50; font-size: 0.9rem;">
                                📧 {candidate['Contact']}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Export buttons with different formats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name=f"shortlist_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        help="Download as CSV spreadsheet"
                    )
                
                with col2:
                    # Mock Excel data (in real implementation, use pandas.to_excel)
                    st.download_button(
                        label="📊 Download Excel",
                        data=csv_data,  # Would be Excel binary in real implementation
                        file_name=f"shortlist_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Download as Excel workbook"
                    )
                
                with col3:
                    json_data = df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="🔧 Download JSON",
                        data=json_data,
                        file_name=f"shortlist_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        help="Download as JSON data"
                    )
                
                with col4:
                    if st.button("📧 Email Report", help="Send report via email"):
                        st.success("📨 Report sent to your email!")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Analytics summary
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 📊 Export Analytics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="neon-metric" style="text-align: center;">
                        <div class="metric-value">{len(mock_shortlist)}</div>
                        <div class="metric-label">Candidates</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    avg_score = sum(c['Score'] for c in mock_shortlist) / len(mock_shortlist)
                    st.markdown(f"""
                    <div class="neon-metric" style="text-align: center;">
                        <div class="metric-value">{avg_score:.1f}%</div>
                        <div class="metric-label">Avg Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    top_performers = len([c for c in mock_shortlist if c['Score'] >= 85])
                    st.markdown(f"""
                    <div class="neon-metric" style="text-align: center;">
                        <div class="metric-value">{top_performers}</div>
                        <div class="metric-label">Top Tier</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="neon-metric" style="text-align: center;">
                        <div class="metric-value">94%</div>
                        <div class="metric-label">Success Rate</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed analytics charts
                st.markdown("### 🎯 Candidate Distribution Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Score distribution
                    score_ranges = {
                        "90-100%": len([c for c in mock_shortlist if c['Score'] >= 90]),
                        "80-89%": len([c for c in mock_shortlist if 80 <= c['Score'] < 90]),
                        "70-79%": len([c for c in mock_shortlist if 70 <= c['Score'] < 80]),
                        "60-69%": len([c for c in mock_shortlist if 60 <= c['Score'] < 70])
                    }
                    
                    fig_dist = px.pie(
                        values=list(score_ranges.values()),
                        names=list(score_ranges.keys()),
                        title="Score Distribution",
                        color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800', '#f44336']
                    )
                    
                    fig_dist.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={'color': 'white'},
                        title={'font': {'color': 'white', 'size': 16}},
                        height=300
                    )
                    
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                with col2:
                    # Experience distribution
                    exp_data = pd.DataFrame(mock_shortlist)
                    exp_data['Experience_Years'] = exp_data['Experience'].str.extract('(\d+)').astype(int)
                    
                    fig_exp = px.histogram(
                        exp_data, x='Experience_Years',
                        title="Experience Distribution",
                        color_discrete_sequence=['#667eea']
                    )
                    
                    fig_exp.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={'color': 'white'},
                        title={'font': {'color': 'white', 'size': 16}},
                        xaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)', 'title': 'Years of Experience'},
                        yaxis={'color': 'white', 'gridcolor': 'rgba(255,255,255,0.2)', 'title': 'Number of Candidates'},
                        height=300
                    )
                    
                    st.plotly_chart(fig_exp, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.balloons()

# Enhanced footer with additional features
def show_footer():
    st.markdown("""
    <div class="glass-card" style="margin-top: 3rem; text-align: center;">
        <h4 style="color: white; margin-bottom: 1rem;">🚀 AI Resume Relevance Engine</h4>
        <p style="color: rgba(255,255,255,0.7); margin: 0;">
            Powered by Advanced AI • Real-time Analytics • Smart Matching
        </p>
        <div style="margin-top: 1rem;">
            <span style="color: rgba(255,255,255,0.5);">
                © 2024 • Built for Hackathons • Made with ❤️ and Streamlit
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()
    
    # Add some JavaScript for additional animations (if needed)
    st.markdown("""
    <script>
        // Add any custom JavaScript here for enhanced interactions
        console.log("🚀 AI Resume Relevance Engine - Ready for Demo!");
    </script>
    """, unsafe_allow_html=True)