import streamlit as st
import json
import os
from datetime import datetime

RESPONSES_FILE = "responses.json"

def save_responses(paper, responses, questions):
    """Save responses for a single paper to session state."""
    filtered_responses = {k: v for k, v in responses.items() if v and str(v).strip()}
    
    st.session_state.responses[str(paper['id'])] = {
        "paper_id": paper['id'],
        "paper_title": paper['title'],
        "responses": responses,
        "questions": questions,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed": len(filtered_responses) == len(questions)
    }

def load_responses(paper_id):
    """Load saved responses for a paper from session state."""
    paper_id_str = str(paper_id)
    if paper_id_str in st.session_state.responses:
        return st.session_state.responses[paper_id_str].get('responses', {})
    return {}

def save_all_responses_to_disk(responses_data):
    """Save the entire responses dictionary to a JSON file."""
    try:
        with open(RESPONSES_FILE, 'w') as f:
            json.dump(responses_data, f, indent=2)
    except Exception as e:
        st.error(f"Failed to save responses to file: {e}")

def load_all_responses_from_disk():
    """Load all responses from the JSON file."""
    if not os.path.exists(RESPONSES_FILE):
        return {}
    try:
        with open(RESPONSES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def export_responses(all_responses):
    """Create a download button for all responses in JSON format."""
    if not all_responses:
        st.warning("No responses to export")
        return
    
    export_data = {
        "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_papers": len(all_responses),
        "responses": all_responses
    }
    
    json_data = json.dumps(export_data, indent=2)
    
    st.download_button(
        label="Download All Responses as JSON",
        data=json_data,
        file_name=f"research_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )