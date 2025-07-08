import streamlit as st
import time
from modules.data_handler import export_responses, load_all_responses_from_disk

def check_password():
    """Returns `True` if the user is logged in, `False` otherwise."""
    # If the user is already logged in, return True
    if st.session_state.get("admin_logged_in"):
        return True

    # --- Login Form ---
    st.title("🔒 Admin Panel Login")
    st.markdown("---")
    
    try:
        # Get credentials from Streamlit secrets
        admin_username = st.secrets["admin_credentials"]["username"]
        admin_password = st.secrets["admin_credentials"]["password"]
    except (KeyError, FileNotFoundError):
        st.error(
            "Admin credentials are not configured. "
            "Please create a `.streamlit/secrets.toml` file."
        )
        return False

    username = st.text_input("Username", key="admin_user")
    password = st.text_input("Password", type="password", key="admin_pass")

    if st.button("Login", key="admin_login_btn"):
        if username == admin_username and password == admin_password:
            st.session_state["admin_logged_in"] = True
            # Rerun the script to reflect the new login state
            st.rerun()
        else:
            st.error("The username or password you entered is incorrect.")
            # Simple delay to mitigate brute-force attacks
            time.sleep(1)
    
    return False

def show_admin_panel():
    """Displays the main content of the admin panel."""
    st.title("🔒 Admin Panel")
    st.markdown("---")
    st.header("Export All User Responses")

    all_responses = load_all_responses_from_disk()

    if all_responses:
        num_papers = len(all_responses)
        total_responses = sum(
            len([v for v in data.get("responses", {}).values() if v and str(v).strip()]) 
            for data in all_responses.values()
        )
        
        st.success(f"Found responses for **{num_papers}** paper(s) with a total of **{total_responses}** answered questions.")
        
        export_responses(all_responses)

    else:
        st.warning("No responses found in `responses.json`. The file is either empty or does not exist.")

# --- Main App Logic ---
st.set_page_config(
    page_title="Admin Panel",
    layout="centered"
)

if check_password():
    show_admin_panel()