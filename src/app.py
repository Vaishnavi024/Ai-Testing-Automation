
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # for `tests` import

import streamlit as st
import asyncio
import json
from io import StringIO

from services.browser_task_runner import BrowserTaskRunner, BrowserTaskExecutionError
from services.config_manager import ConfigManager
from utils.history_cleaner import HistoryCleaner
from tests.predefined_tests import PREDEFINED_TESTS

# Redirect logs
log_stream = StringIO()
sys.stdout = sys.stderr = log_stream

logo_path = Path(__file__).parent.parent / "assets" / "pyngTest.png"

# Streamlit config
st.set_page_config(page_title="PyngTest Agent", page_icon=str(logo_path), layout="wide")

# ✨ Styling
st.markdown("""
    <style>
    html, body, .stApp {
        background: linear-gradient(140deg, #1f1911, #f5ae51);
        background-attachment: fixed;
    }

    .stTextInput, .stTextArea, .stSelectbox, .stCheckbox, .stButton > button {
        font-size: 15px !important;
    }

    .stButton > button {
        background-color: #ff6600 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }

    .test-result-box {
        white-space: pre-wrap;
        background-color: #fff7e6;
        padding: 1rem;
        border-radius: 10px;
        font-size: 15px;
        color: #111;
    }

    .fail-box {
        background-color: #fff3cd;
        color: #856404;
    }

    .stMultiSelect:hover, .stButton > button:hover {
        opacity: 0.9;
        box-shadow: 0 0 8px rgba(255, 102, 0, 0.6);
    }
</style>

""", unsafe_allow_html=True)

# Page header
st.image(str(logo_path), width=70)
st.title("🚀 PyngTest Agent")
st.caption("Automate Pyng's web UI tests visually — no coding needed!")

# Sidebar
config_manager = ConfigManager()
with st.sidebar:
    st.image(logo_path, width=80)
    st.header("⚙️ Settings")
    model_provider = st.selectbox("Model Provider", ["google", "openai", "anthropic"])
    model_name = st.text_input("Model Name", value="gemini-2.0-flash")
    use_vision = st.checkbox("Use Vision", value=True)  

    api_key_key = f"{model_provider.upper()}_API_KEY"
    api_key = config_manager.get_config(api_key_key)
    show_key = st.toggle("🔐 Show API Key", value=False)
    st.text_input(f"{model_provider.capitalize()} API Key (.env)", value=api_key if show_key else "*" * len(api_key), disabled=True)

# Instruction
instruction = st.text_area("Enter a test instruction")

# Extract result utility
def extract_final_result(data):
    if isinstance(data, dict) and "final_result" in data:
        return data["final_result"]

    if isinstance(data, dict) and "history" in data:
        for entry in reversed(data["history"]):
            if not isinstance(entry, dict): continue
            actions = entry.get("model_output", {}).get("action", [])
            if isinstance(actions, dict): actions = [actions]
            for action in actions:
                done_block = action.get("done")
                if isinstance(done_block, dict):
                    return done_block.get("text")
                elif isinstance(done_block, str):
                    return done_block
    return None

# ▶️ Run Test (Single)
if st.button("Run Test"):
    if not instruction.strip():
        st.warning("⚠️ Please enter a test instruction.")
    else:
        config_manager.set_config("MODEL_PROVIDER", model_provider)
        config_manager.set_config("MODEL_NAME", model_name)
        config_manager.set_config("USE_VISION", str(use_vision).lower())

        with st.spinner("🧠 Executing browser task..."):
            runner = BrowserTaskRunner()
            try:
                history_path, timestamp = asyncio.run(runner.execute_task(instruction))
                cleaned_path = Path(history_path).parent / f"cleaned_history_{timestamp}.json"
                HistoryCleaner().clean_history(history_path, str(cleaned_path))

                final_result = None
                with open(cleaned_path, "r") as f:
                    data = json.load(f)
                    final_result = extract_final_result(data)

                st.markdown("### 🧠 Final Agent Result:")
                if final_result:
                    st.markdown(f"<div class='test-result-box'>{final_result}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<div class='test-result-box fail-box'>⚠️ No final_result field found.</div>",
                        unsafe_allow_html=True
                    )

                log_output = log_stream.getvalue()
                if log_output:
                    with st.expander("📋 Full Execution Logs"):
                        st.text(log_output)

            except BrowserTaskExecutionError as e:
                st.error(f"❌ Task Failed: {str(e)}")
            finally:
                asyncio.run(runner.close())

# 🔁 MULTI TEST EXECUTION
st.markdown("---")
st.subheader("Run Multiple Predefined Test Cases")

selected_tests = st.multiselect("🧪 Select Test Cases", options=list(PREDEFINED_TESTS.keys()), default=[])

if st.button("🚀 Run Selected Tests"):
    runner = BrowserTaskRunner()
    for test_name in selected_tests:
        st.markdown(f"---\n### 🧪 Running: **{test_name}**")
        task = PREDEFINED_TESTS[test_name]
        try:
            history_path, timestamp = asyncio.run(runner.execute_task(task))
            cleaned_path = Path(history_path).parent / f"cleaned_history_{timestamp}.json"
            HistoryCleaner().clean_history(history_path, str(cleaned_path))

            final_result = None
            with open(cleaned_path, "r") as f:
                data = json.load(f)
                final_result = extract_final_result(data)

            st.markdown("### Final Agent Result:")
            if final_result:
                st.markdown(f"<div class='test-result-box'>{final_result}</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div class='test-result-box fail-box'>⚠️ Final result not found.</div>",
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"❌ Failed test '{test_name}': {e}")
    asyncio.run(runner.close())
