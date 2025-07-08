import streamlit as st
from modules.data_handler import export_responses, load_all_responses_from_disk

st.set_page_config(
    page_title="Admin Panel",
    layout="centered"
)

st.title("🔒 Admin Panel")
st.markdown("---")
st.header("Export All User Responses")

all_responses = load_all_responses_from_disk()

if all_responses:
    num_papers = len(all_responses)
    
    total_responses = sum(len([v for v in data.get("responses", {}).values() if v and str(v).strip()]) for data in all_responses.values())
    
    st.success(f"Found responses for **{num_papers}** paper(s) with a total of **{total_responses}** answered questions.")
    
    export_responses(all_responses)

else:
    st.warning("No responses found in `responses.json`. The file is either empty or does not exist.")