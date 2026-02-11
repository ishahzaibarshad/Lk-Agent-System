"""
NSOL BPO - Professional Streamlit Dashboard
Run: streamlit run streamlit_app.py
"""
import os
import sys
import requests
from pathlib import Path

# Ensure project root
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

import streamlit as st

# Page config - first Streamlit command
st.set_page_config(
    page_title="NSOL BPO Dashboard",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
    h1 { color: #1e3a5f; font-weight: 700; border-bottom: 2px solid #3b82f6; padding-bottom: 0.3em; }
    h2 { color: #334155; font-weight: 600; margin-top: 1.5rem; }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1rem 1.25rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .sidebar .sidebar-content { background: linear-gradient(180deg, #1e3a5f 0%, #0f172a 100%); }
    hr { margin: 2rem 0; border-color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)


def get_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def fetch_ngrok_url():
    try:
        r = requests.get(f"{API_BASE}/api/ngrok-url", timeout=2)
        if r.ok and r.json().get("url"):
            return r.json()["url"]
    except Exception:
        pass
    return None


def login(email: str, password: str):
    try:
        r = requests.post(
            f"{API_BASE}/api/auth/login",
            data={"username": email, "password": password},
            timeout=10,
        )
        if r.status_code == 200:
            st.session_state["token"] = r.json()["access_token"]
            st.session_state["user_email"] = email
            return True
    except Exception as e:
        st.error(f"Login failed: {e}")
    return False


def ensure_logged_in():
    if st.session_state.get("token"):
        return True
    with st.form("login_form"):
        st.markdown("### Sign in to NSOL BPO Dashboard")
        email = st.text_input("Email", value="admin@nsolbpo.com", type="default")
        password = st.text_input("Password", type="password", value="admin123")
        if st.form_submit_button("Login"):
            if login(email, password):
                st.rerun()
            else:
                st.error("Invalid credentials.")
    return False


def main():
    if not ensure_logged_in():
        return

    # Sidebar
    with st.sidebar:
        st.markdown("## 📞 NSOL BPO")
        st.markdown("---")
        page = st.radio(
            "Menu",
            ["Dashboard", "Agents", "Contacts", "Calls", "Bookings"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.caption("Ngrok URL (for calls)")
        ngrok_sidebar = st.text_input(
            "Ngrok URL",
            value=st.session_state.get("ngrok_url") or fetch_ngrok_url() or "",
            placeholder="https://xxxx.ngrok-free.app",
            label_visibility="collapsed",
        )
        if ngrok_sidebar:
            st.session_state["ngrok_url"] = ngrok_sidebar.strip().rstrip("/")
        st.markdown("---")
        st.caption(st.session_state.get("user_email", ""))
        if st.button("Logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    headers = get_headers()

    if page == "Dashboard":
        st.title("Dashboard")
        try:
            r = requests.get(f"{API_BASE}/api/dashboard/stats", headers=headers, timeout=5)
            if r.status_code == 200:
                d = r.json()
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    st.metric("Agents", d["total_agents"])
                with c2:
                    st.metric("Contacts", d["total_contacts"])
                with c3:
                    st.metric("Calls", d["total_calls"])
                with c4:
                    st.metric("Bookings", d["total_bookings"])
                with c5:
                    st.metric("Success Rate", f"{d['success_rate']}%")
            else:
                st.warning("Could not load stats.")
        except Exception as e:
            st.error(f"API error: {e}. Is the server running at {API_BASE}?")

    elif page == "Agents":
        st.title("Agents")
        try:
            r = requests.get(f"{API_BASE}/api/agents", headers=headers, timeout=5)
            if r.status_code == 200:
                agents = r.json().get("agents", [])
                with st.expander("➕ New Agent"):
                    with st.form("new_agent"):
                        name = st.text_input("Name", placeholder="e.g. Merideth")
                        voice_id = st.text_input("Voice ID (optional)")
                        is_active = st.checkbox("Active", value=True)
                        if st.form_submit_button("Create"):
                            rr = requests.post(
                                f"{API_BASE}/api/agents",
                                json={"name": name, "voice_id": voice_id or None, "is_active": is_active},
                                headers=headers,
                                timeout=5,
                            )
                            if rr.status_code == 201:
                                st.success("Agent created.")
                                st.rerun()
                            else:
                                st.error(rr.text or "Failed")
                if agents:
                    st.dataframe(
                        [{"ID": a["id"], "Name": a["name"], "Active": a["is_active"]} for a in agents],
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("No agents yet. Create one above.")
            else:
                st.warning("Could not load agents.")
        except Exception as e:
            st.error(str(e))

    elif page == "Contacts":
        st.title("Contacts")
        ngrok_auto = fetch_ngrok_url()
        if ngrok_auto:
            st.success(f"Ngrok URL auto-detected. Calls will use it automatically.")
        else:
            st.info("Ngrok not detected. You may be prompted for URL when calling, or set NGROK_BASE_URL in .env")
        try:
            r = requests.get(f"{API_BASE}/api/contacts?page_size=100", headers=headers, timeout=5)
            if r.status_code == 200:
                contacts = r.json().get("contacts", [])
                col1, col2 = st.columns([1, 3])
                with col1:
                    with st.expander("➕ New Contact"):
                        with st.form("new_contact"):
                            name = st.text_input("Name")
                            phone = st.text_input("Phone (E.164)", placeholder="+14155551234")
                            email = st.text_input("Email (optional)")
                            if st.form_submit_button("Create"):
                                rr = requests.post(
                                    f"{API_BASE}/api/contacts",
                                    json={"name": name, "phone": phone, "email": email or None},
                                    headers=headers,
                                    timeout=5,
                                )
                                if rr.status_code == 201:
                                    st.success("Contact created.")
                                    st.rerun()
                                else:
                                    st.error(rr.json().get("detail", rr.text))
                    st.markdown("**Import CSV**")
                    csv_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
                    if csv_file and st.button("Import"):
                        rr = requests.post(
                            f"{API_BASE}/api/contacts/import/csv",
                            files={"file": (csv_file.name, csv_file.getvalue(), "text/csv")},
                            headers=headers,
                            timeout=15,
                        )
                        if rr.status_code == 200:
                            j = rr.json()
                            st.success(f"Imported: {j.get('success', 0)} ok, {j.get('failed', 0)} failed.")
                            st.rerun()
                        else:
                            st.error(rr.text or "Import failed")
                with col2:
                    if contacts:
                        for c in contacts:
                            with st.container():
                                row = st.columns([3, 2, 2, 1])
                                row[0].markdown(f"**{c['name']}**")
                                row[1].markdown(c.get("phone", ""))
                                row[2].markdown(c.get("email") or "-")
                                if row[3].button("Call", key=f"call_{c['id']}"):
                                    ngrok_url = (ngrok_auto or st.session_state.get("ngrok_url") or "").strip().rstrip("/")
                                    if ngrok_url:
                                        try:
                                            ar = requests.get(f"{API_BASE}/api/agents", headers=headers, timeout=5)
                                            agents = ar.json().get("agents", []) if ar.ok else []
                                            if not agents:
                                                st.error("No agents. Create an agent first.")
                                            else:
                                                cr = requests.post(
                                                    f"{API_BASE}/api/outbound/call",
                                                    json={"agent_id": agents[0]["id"], "contact_id": c["id"], "ngrok_url": ngrok_url},
                                                    headers=headers,
                                                    timeout=10,
                                                )
                                                if cr.status_code == 200 and cr.json().get("success") != False:
                                                    st.success("Call initiated! SID: " + str(cr.json().get("call_sid")))
                                                    st.session_state["ngrok_url"] = ngrok_url
                                                    st.rerun()
                                                else:
                                                    j = cr.json() if cr.headers.get("content-type", "").startswith("application/json") else {}
                                                    err = j.get("detail") or j.get("error") or cr.text or "Call failed"
                                                    st.error("Call failed: " + str(err))
                                        except Exception as e:
                                            err = getattr(e, "response", None)
                                            if err is not None and hasattr(err, "json") and callable(err.json):
                                                try:
                                                    j = err.json()
                                                    st.error("Call failed: " + str(j.get("detail") or j.get("error", str(e))))
                                                except Exception:
                                                    st.error(str(e))
                                            else:
                                                st.error(str(e))
                                    else:
                                        st.warning("Set Ngrok URL in sidebar (once) or NGROK_BASE_URL in .env.")
                                st.divider()
                    else:
                        st.info("No contacts. Add one or import CSV.")
            else:
                st.warning("Could not load contacts.")
        except Exception as e:
            st.error(str(e))

    elif page == "Calls":
        st.title("Call History")
        try:
            r = requests.get(f"{API_BASE}/api/calls?page_size=50", headers=headers, timeout=5)
            if r.status_code == 200:
                calls = r.json().get("calls", [])
                if calls:
                    rows = []
                    for c in calls:
                        rows.append({
                            "ID": c.get("id"),
                            "SID": (c.get("call_sid") or "")[:20] + "..." if c.get("call_sid") else "-",
                            "Status": c.get("status", "-"),
                            "Duration": str(c.get("duration") or 0) + "s",
                            "Outcome": c.get("outcome") or "-",
                        })
                    st.dataframe(rows, use_container_width=True, hide_index=True)
                else:
                    st.info("No calls yet.")
            else:
                st.warning("Could not load calls.")
        except Exception as e:
            st.error(str(e))

    elif page == "Bookings":
        st.title("Bookings")
        try:
            r = requests.get(f"{API_BASE}/api/bookings?page_size=50", headers=headers, timeout=5)
            if r.status_code == 200:
                bookings = r.json().get("bookings", [])
                if bookings:
                    rows = []
                    for b in bookings:
                        rows.append({
                            "ID": b.get("id"),
                            "Contact ID": b.get("contact_id"),
                            "Meeting": str(b.get("meeting_time", ""))[:16],
                            "Status": b.get("status", "-"),
                        })
                    st.dataframe(rows, use_container_width=True, hide_index=True)
                else:
                    st.info("No bookings yet.")
            else:
                st.warning("Could not load bookings.")
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()
