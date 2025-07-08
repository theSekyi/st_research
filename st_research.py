import streamlit as st
from modules.config import load_config
from modules.ui_components import inject_custom_css, render_sidebar, render_question, render_progress_bar
from modules.pdf_viewer import render_pdf_viewer
from modules.data_handler import save_responses, load_responses, load_all_responses_from_disk, save_all_responses_to_disk
from modules.config import get_questions_for_paper

# --- Page Configuration ---
st.set_page_config(
    page_title="Research Paper Review Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
inject_custom_css()

# --- Load Configuration ---
config = load_config()
papers = config.get("papers", [])
question_templates = config.get("question_templates", {})

# --- Initialize Session State ---
if 'responses' not in st.session_state:
    st.session_state.responses = load_all_responses_from_disk()
if 'current_paper_id' not in st.session_state:
    st.session_state.current_paper_id = None

# --- Sidebar for Paper Selection ---
selected_paper = render_sidebar(papers, question_templates)

# --- Main Content Area ---
if not selected_paper:
    st.title("Welcome to the Research Paper Review Tool")
    st.markdown("Please select a paper from the sidebar to begin.")
    st.info("Your progress is saved automatically.")
else:
    # --- UI for Resizing Columns ---
    st.sidebar.markdown("---")
    pdf_width = st.sidebar.slider(
        "Adjust PDF Viewer Width (%)", 
        min_value=20, 
        max_value=80, 
        value=50, 
        step=5,
        key="pdf_width_slider"
    )
    question_width = 100 - pdf_width
    
    # --- Two-Column Layout ---
    q_col, pdf_col = st.columns((question_width, pdf_width))

    # --- PDF Viewer Column ---
    with pdf_col:
        st.markdown('<div class="scrollable-column pdf-column">', unsafe_allow_html=True)
        st.subheader(f"📄 {selected_paper['title']}")
        st.markdown("---")
        render_pdf_viewer(selected_paper)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Questions & Responses Column ---
    with q_col:
        st.markdown('<div class="scrollable-column">', unsafe_allow_html=True)
        st.subheader("📝 Review Questions")
        st.markdown("---")
        
        all_questions = get_questions_for_paper(selected_paper['id'], question_templates)
        loaded_responses = load_responses(selected_paper['id'])
        
        # --- Progress Bar ---
        answered_count = len([r for r in loaded_responses.values() if r and str(r).strip()])
        total_questions = len(all_questions)
        progress = (answered_count / total_questions) if total_questions > 0 else 0
        render_progress_bar(progress, answered_count, total_questions)
        st.markdown("---")
        
        # --- Render Questions and Capture Responses ---
        current_responses = {}
        for category in question_templates.keys():
            category_questions = [q for q in all_questions if q['category'] == category]
            if category_questions:
                with st.expander(f"**{category.capitalize()}**", expanded=True):
                    for q in category_questions:
                        q_key = f"q_{q['id']}"
                        saved_value = loaded_responses.get(q_key)
                        response = render_question(q, saved_value, selected_paper['id'])
                        current_responses[q_key] = response

        # --- Save responses and write to disk ---
        save_responses(selected_paper, current_responses, all_questions)
        save_all_responses_to_disk(st.session_state.responses)
        st.markdown('</div>', unsafe_allow_html=True)