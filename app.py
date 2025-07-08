import streamlit as st
from modules.config import load_config, get_questions_for_paper
from modules.data_handler import (
    save_responses,
    load_responses,
    load_all_responses_from_disk,
    save_all_responses_to_disk
)
from modules.pdf_viewer import render_pdf_viewer
from modules.ui_components import (
    inject_custom_css,
    render_sidebar,
    render_question,
    render_progress_bar
)

st.set_page_config(
    page_title="Reviewer Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

config = load_config()
papers = config.get('papers', [])
question_templates = config.get('question_templates', {})

if 'responses' not in st.session_state:
    st.session_state.responses = load_all_responses_from_disk()

selected_paper = render_sidebar(papers, question_templates)

if selected_paper:
    all_questions = get_questions_for_paper(selected_paper['id'], question_templates)
    saved_responses = load_responses(selected_paper['id'])
    
    left_col, right_col = st.columns([6, 5], gap="large")

    with right_col:
        st.subheader(f"📄 {selected_paper['title']}")
        render_pdf_viewer(selected_paper)

    with left_col:
        with st.form(key=f"analysis_form_{selected_paper['id']}"):
            questions_by_category = {}
            for q in all_questions:
                category = q.get('category', 'general')
                if category not in questions_by_category:
                    questions_by_category[category] = []
                questions_by_category[category].append(q)

            category_keys = list(questions_by_category.keys())
            category_tabs = st.tabs([cat.capitalize() for cat in category_keys])
            
            current_responses = {}

            for i, category in enumerate(category_keys):
                with category_tabs[i]:
                    questions_in_category = questions_by_category[category]
                    st.header(f"{category.capitalize()} ({len(questions_in_category)} questions)")
                    
                    for question in questions_in_category:
                        q_id_str = str(question['id'])
                        saved_value = saved_responses.get(q_id_str)
                        response = render_question(question, saved_value, selected_paper['id'])
                        current_responses[q_id_str] = response
            
            submitted = st.form_submit_button("💾 Save Progress")
            
            if submitted:
                save_responses(selected_paper, current_responses, all_questions)
                save_all_responses_to_disk(st.session_state.responses)
                st.toast("✅ Your progress has been saved!", icon="🎉")

        answered_count = len([r for r in load_responses(selected_paper['id']).values() if r and str(r).strip()])
        total_questions = len(all_questions)
        progress = answered_count / total_questions if total_questions > 0 else 0
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Analysis Progress")
        render_progress_bar(progress, answered_count, total_questions)

else:
    st.markdown("## 📚 Welcome to the Research Paper Analysis Platform")
    st.info("To begin, select a paper from the sidebar to review.")