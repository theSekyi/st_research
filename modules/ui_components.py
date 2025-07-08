import streamlit as st
from modules.config import get_questions_for_paper

def inject_custom_css():
    """Injects custom CSS to override default Streamlit styles."""
    st.markdown("""
        <style>
            /* Hide Streamlit's default header and footer */
            .st-emotion-cache-18ni7ap, .st-emotion-cache-h4xjwg {
                display: none;
            }
            header[data-testid="stHeader"] {
                display: none;
            }
            footer {
                display: none;
            }
            
            /* Clean up the multi-page sidebar */
            .st-emotion-cache-1y4p8pa {
                padding-top: 2rem;
            }
            
            /* Custom styling for tabs */
            .st-emotion-cache-1h9usn1 a {
                padding: 0.5em 1em;
                border-radius: 8px 8px 0 0;
                transition: background-color 0.3s, color 0.3s;
            }
            button[data-baseweb="tab"][aria-selected="true"] {
                background-color: #262730;
                border-bottom: 3px solid #FF4B4B;
                color: white;
            }
            button[data-baseweb="tab"] {
                background-color: transparent;
                border-bottom: 3px solid transparent;
            }
            .stTabs {
                border-bottom: 1px solid #444;
            }
        </style>
    """, unsafe_allow_html=True)

def get_paper_status_icon(paper_id, all_questions):
    """Returns a status icon based on the paper's review progress."""
    if str(paper_id) not in st.session_state.responses:
        return "⚪"
    
    paper_data = st.session_state.responses[str(paper_id)]
    responses = paper_data.get("responses", {})
    answered_count = len([r for r in responses.values() if r and str(r).strip()])

    if answered_count == 0:
        return "⚪"
    elif answered_count >= len(all_questions):
        return "✅"
    else:
        return "📝"

def render_sidebar(papers, question_templates):
    """Renders the sidebar for paper selection on the main page."""
    st.sidebar.markdown("## 📝 Select a Paper")
    st.sidebar.markdown("---")
    
    selected_paper = None
    
    for i, paper in enumerate(papers):
        all_questions_for_paper = get_questions_for_paper(paper['id'], question_templates)
        icon = get_paper_status_icon(paper['id'], all_questions_for_paper)
        
        if st.sidebar.button(f"{i + 1}. {icon} {paper['title']}", key=f"paper_btn_{paper['id']}", use_container_width=True):
            st.session_state.current_paper_id = paper['id']
    
    if st.session_state.get('current_paper_id'):
        selected_paper = next((p for p in papers if p['id'] == st.session_state.current_paper_id), None)

    return selected_paper

def render_progress_bar(progress, answered, total):
    """Render progress bar with stats."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.progress(progress)
    
    with col2:
        st.markdown(f"**{answered}/{total}** answered")

def render_question(question, saved_value, paper_id):
    """Render a single question based on its type."""
    q_id = question['id']
    q_text = question['text']
    q_type = question['type']
    
    st.markdown(f"**Q{q_id + 1}:** {q_text}")
    
    response = None
    
    if q_type == "text":
        response = st.text_area(
            "",
            value=saved_value or "",
            height=100,
            key=f"paper_{paper_id}_q{q_id}",
            placeholder="Enter your response...",
            label_visibility="collapsed"
        )
    elif q_type == "multiple_choice":
        options = question.get('options', [])
        default_idx = options.index(saved_value) if saved_value in options else 0
        response = st.selectbox(
            "",
            options=options,
            index=default_idx,
            key=f"paper_{paper_id}_q{q_id}",
            label_visibility="collapsed"
        )
    elif q_type == "rating":
        min_val = question.get('min', 1)
        max_val = question.get('max', 5)
        default_val = int(saved_value) if saved_value and str(saved_value).isdigit() else min_val
        
        response = st.slider(
            "",
            min_value=min_val,
            max_value=max_val,
            value=default_val,
            key=f"paper_{paper_id}_q{q_id}",
            label_visibility="collapsed"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    return response