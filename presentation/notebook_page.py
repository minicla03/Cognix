import streamlit as st
import uuid
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag_logic.memory.NotebookManger import NotebookManager

notebook_manager = NotebookManager()
user_id = "73776694-e8b0-4014-92c9-0db7540a38d6"

st.set_page_config(page_title="Cognix - Notebook", layout="wide")

st.title("📚 Cognix - I tuoi Notebook")
st.markdown("Crea nuovi notebook o apri quelli esistenti per avviare una sessione RAG.")

# --- Stato iniziale ---
if "notebooks" not in st.session_state:
    st.session_state.notebooks = {}

    notebooks = notebook_manager.retrieve_notebook_by_user(user_id)

    if len(notebooks) == 0:
        st.warning("Nessun notebook disponibile")

    for notebook in notebooks:
        st.session_state.notebooks[notebook.id_notebook] = notebook

# --- Funzione creazione notebook ---
def create_notebook(notebook_namea):
    nb_c= notebook_manager.create_notebook(notebook_namea, user_id)
    st.session_state.notebooks[nb_c.id_notebook] = nb_c
    return nb_c

# --- Sezione creazione notebook ---
st.subheader("➕ Crea un nuovo notebook")
with st.form("create_form"):
    notebook_name = st.text_input("Titolo notebook", placeholder="Inserisci il nome del notebook...")
    submitted = st.form_submit_button("Crea")
    if submitted:
        if notebook_name.strip():
            create_notebook(notebook_name)
            st.success(f"Notebook '{notebook_name}' creato con successo!")
        else:
            st.warning("Inserisci un titolo valido.")

st.markdown("---")
st.subheader("📖 Notebook disponibili")

# --- Sezione visualizzazione notebook ---
if st.session_state.notebooks:

    for nb_id, nb in st.session_state.notebooks.items():
        with st.container():
            st.markdown(
                f"""
                <div style='border:1px solid #ddd; border-radius:10px; padding:15px; margin-bottom:10px;'>
                    <b>{nb.notebook_name}</b><br>
                    <span style='font-size:0.8em;color:gray;'>Creato il {nb.created_at}</span><br><br>
                    <a href='/chat?notebook_id={nb_id}' target='_self'>
                        <button style='background-color:#0078D4;color:white;padding:6px 12px;border:none;border-radius:6px;'>Apri Notebook</button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("Nessun notebook creato finora.")