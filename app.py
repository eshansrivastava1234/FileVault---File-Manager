"""
FileVault — A clean Streamlit UI for basic file CRUD operations
(Create, Read, Update, Delete) built on top of a simple Python
file-handling backend.

Run with:
    streamlit run app.py
"""

import os
from pathlib import Path
from datetime import datetime

import streamlit as st

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
WORKDIR = Path("filevault_storage")
WORKDIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="FileVault — File Manager",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        .main {
            background: radial-gradient(circle at top left, #f6f8ff 0%, #ffffff 45%);
        }

        .fv-hero {
            padding: 2.1rem 2.4rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #ec4899 100%);
            color: white;
            margin-bottom: 1.6rem;
            box-shadow: 0 12px 30px rgba(79, 70, 229, 0.25);
        }
        .fv-hero h1 {
            margin: 0;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }
        .fv-hero p {
            margin: 0.35rem 0 0 0;
            opacity: 0.92;
            font-size: 1.02rem;
        }

        .fv-card {
            background: white;
            border: 1px solid #eef0f6;
            border-radius: 16px;
            padding: 1.5rem 1.6rem;
            box-shadow: 0 4px 18px rgba(20, 20, 43, 0.04);
            margin-bottom: 1rem;
        }

        .fv-badge {
            display: inline-block;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            background: #eef2ff;
            color: #4338ca;
            margin-bottom: 0.6rem;
        }

        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.1rem;
            border: none;
            transition: transform 0.08s ease-in-out;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
        }

        .fv-primary button {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
        }

        section[data-testid="stSidebar"] {
            background: #14142b;
        }
        section[data-testid="stSidebar"] * {
            color: #e5e5f5 !important;
        }
        section[data-testid="stSidebar"] .stRadio label {
            font-weight: 500;
        }

        .fv-filelist {
            font-family: 'Menlo', 'Consolas', monospace;
            font-size: 0.85rem;
            background: #0f172a;
            color: #a5f3fc;
            padding: 1rem;
            border-radius: 12px;
            max-height: 260px;
            overflow-y: auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Helpers (the actual file-handling logic)
# --------------------------------------------------------------------------
def list_files():
    return sorted([p for p in WORKDIR.iterdir() if p.is_file()])


def safe_path(name: str) -> Path:
    """Keep every operation confined to the WORKDIR sandbox."""
    return WORKDIR / Path(name).name


def create_file(name: str, content: str):
    path = safe_path(name)
    if path.exists():
        return False, f"'{name}' already exists."
    path.write_text(content, encoding="utf-8")
    return True, f"'{name}' created successfully."


def read_file(name: str):
    path = safe_path(name)
    if not path.exists():
        return False, "File does not exist.", None
    return True, "File read successfully.", path.read_text(encoding="utf-8")


def rename_file(name: str, new_name: str):
    path = safe_path(name)
    if not path.exists():
        return False, "File does not exist."
    new_path = safe_path(new_name)
    if new_path.exists():
        return False, f"'{new_name}' already exists."
    path.rename(new_path)
    return True, f"Renamed '{name}' → '{new_name}'."


def overwrite_file(name: str, content: str):
    path = safe_path(name)
    if not path.exists():
        return False, "File does not exist."
    path.write_text(content, encoding="utf-8")
    return True, f"'{name}' overwritten successfully."


def append_file(name: str, content: str):
    path = safe_path(name)
    if not path.exists():
        return False, "File does not exist."
    with open(path, "a", encoding="utf-8") as fs:
        fs.write(content)
    return True, f"Content appended to '{name}'."


def delete_file(name: str):
    path = safe_path(name)
    if not path.exists():
        return False, "File does not exist."
    path.unlink()
    return True, f"'{name}' deleted successfully."


# --------------------------------------------------------------------------
# Hero header
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="fv-hero">
        <h1>🗂️ FileVault</h1>
        <p>A simple, elegant file management dashboard — Create, Read, Update & Delete files with ease.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Sidebar navigation
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Operations")
    action = st.radio(
        "Choose an action",
        ["📄 Create", "📖 Read", "✏️ Update", "🗑️ Delete"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### 📂 Files in vault")
    files = list_files()
    if files:
        listing = "\n".join(f"• {f.name}  ({f.stat().st_size} B)" for f in files)
    else:
        listing = "No files yet."
    st.markdown(f'<div class="fv-filelist">{listing}</div>', unsafe_allow_html=True)
    st.caption(f"Storage folder: `{WORKDIR}/`")

# --------------------------------------------------------------------------
# Main panel
# --------------------------------------------------------------------------
col_main, col_side = st.columns([2.2, 1])

with col_main:
    # ---------------- CREATE ----------------
    if action == "📄 Create":
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<span class="fv-badge">CREATE</span>', unsafe_allow_html=True)
        st.subheader("Create a new file")
        name = st.text_input("File name", placeholder="e.g. notes.txt")
        content = st.text_area("File content", placeholder="Type what you want to write...", height=180)
        if st.button("🚀 Create File", type="primary"):
            if not name.strip():
                st.warning("Please enter a file name.")
            else:
                ok, msg = create_file(name.strip(), content)
                st.success(msg) if ok else st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- READ ----------------
    elif action == "📖 Read":
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<span class="fv-badge">READ</span>', unsafe_allow_html=True)
        st.subheader("Read a file")
        names = [f.name for f in list_files()]
        if names:
            name = st.selectbox("Select a file", names)
        else:
            name = st.text_input("File name", placeholder="e.g. notes.txt")
        if st.button("🔍 Read File", type="primary"):
            ok, msg, data = read_file(name)
            if ok:
                st.success(msg)
                st.code(data if data else "(empty file)", language="text")
            else:
                st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- UPDATE ----------------
    elif action == "✏️ Update":
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<span class="fv-badge">UPDATE</span>', unsafe_allow_html=True)
        st.subheader("Update a file")
        names = [f.name for f in list_files()]
        if names:
            name = st.selectbox("Select a file", names)
        else:
            name = st.text_input("File name", placeholder="e.g. notes.txt")

        mode = st.radio(
            "What would you like to do?",
            ["Rename", "Overwrite", "Append"],
            horizontal=True,
        )

        if mode == "Rename":
            new_name = st.text_input("New file name", placeholder="e.g. renamed.txt")
            if st.button("✅ Rename", type="primary"):
                ok, msg = rename_file(name, new_name)
                st.success(msg) if ok else st.error(msg)

        elif mode == "Overwrite":
            content = st.text_area("New content (replaces existing content)", height=180)
            if st.button("✅ Overwrite", type="primary"):
                ok, msg = overwrite_file(name, content)
                st.success(msg) if ok else st.error(msg)

        elif mode == "Append":
            content = st.text_area("Content to append", height=140)
            if st.button("✅ Append", type="primary"):
                ok, msg = append_file(name, content)
                st.success(msg) if ok else st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DELETE ----------------
    elif action == "🗑️ Delete":
        st.markdown('<div class="fv-card">', unsafe_allow_html=True)
        st.markdown('<span class="fv-badge">DELETE</span>', unsafe_allow_html=True)
        st.subheader("Delete a file")
        names = [f.name for f in list_files()]
        if names:
            name = st.selectbox("Select a file", names)
        else:
            name = st.text_input("File name", placeholder="e.g. notes.txt")

        confirm = st.checkbox("I understand this action cannot be undone.")
        if st.button("🗑️ Delete File", disabled=not confirm, type="primary"):
            ok, msg = delete_file(name)
            st.success(msg) if ok else st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)

with col_side:
    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Vault stats")
    files = list_files()
    total_size = sum(f.stat().st_size for f in files)
    c1, c2 = st.columns(2)
    c1.metric("Files", len(files))
    c2.metric("Total size", f"{total_size} B")
    if files:
        latest = max(files, key=lambda f: f.stat().st_mtime)
        st.caption(
            f"Last modified: **{latest.name}**  \n"
            f"{datetime.fromtimestamp(latest.stat().st_mtime).strftime('%d %b %Y, %H:%M')}"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="fv-card">', unsafe_allow_html=True)
    st.markdown("#### ℹ️ About")
    st.write(
        "FileVault wraps simple Python `pathlib`/file-I/O operations "
        "(create, read, rename, overwrite, append, delete) in a clean "
        "Streamlit interface. All files are kept sandboxed inside the "
        "`filevault_storage/` folder for safety."
    )
    st.markdown("</div>", unsafe_allow_html=True)