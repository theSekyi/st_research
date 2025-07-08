import streamlit as st
import base64
import os
import requests

try:
    from streamlit_pdf_viewer import pdf_viewer
    PDF_VIEWER_AVAILABLE = True
except ImportError:
    PDF_VIEWER_AVAILABLE = False

@st.cache_data(show_spinner="Fetching PDF...")
def fetch_pdf_from_url(url):
    """Fetch PDF content from a URL and return its bytes."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch PDF: {e}")
        return None

def render_pdf_viewer(paper):
    """Render PDF viewer for the paper with robust fetching."""
    pdf_url = paper.get('pdf_url', '')
    local_pdf = paper.get('local_pdf', None)
    
    if "ncbi.nlm.nih.gov" in pdf_url:
        st.info("This PDF from PubMed Central cannot be embedded directly due to security policies.")
        st.link_button("📄 Open PDF in New Tab", pdf_url, use_container_width=True)
        render_pdf_upload_option()
        return

    if pdf_url:
        pdf_bytes = fetch_pdf_from_url(pdf_url)
        if pdf_bytes and PDF_VIEWER_AVAILABLE:
            # Set a large height; the parent div will handle scrolling
            pdf_viewer(pdf_bytes, height=1200)
        elif pdf_bytes:
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            # Set a large height in pixels for the iframe
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1200px" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.warning("Could not display the PDF. Please try opening it in a new tab or uploading a local copy.")
            st.link_button("📄 Open PDF in New Tab", pdf_url, use_container_width=True)
            render_pdf_upload_option()

    elif local_pdf and os.path.exists(local_pdf):
        render_local_pdf(local_pdf)
    
    else:
        st.warning("No PDF source provided for this paper.")
        render_pdf_upload_option()

def render_local_pdf(pdf_path):
    """Render local PDF file."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            if PDF_VIEWER_AVAILABLE:
                pdf_viewer(pdf_bytes, height=1200)
            else:
                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1200px" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading local PDF: {e}")

def render_pdf_upload_option():
    """Render an option to upload a PDF locally."""
    st.markdown("---")
    st.markdown("**Or, upload a local copy of the PDF:**")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        key=f"pdf_upload_{st.session_state.get('current_paper_id', 0)}"
    )
    
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.getvalue()
        if PDF_VIEWER_AVAILABLE:
            pdf_viewer(pdf_bytes, height=1200)
        else:
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1200px" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)