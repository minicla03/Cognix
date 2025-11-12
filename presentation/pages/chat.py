import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from rag_logic.memory.ChatManager import ChatManager

st.set_page_config(
    page_title="Cognix - Workspace",
    page_icon="👁️‍🗨️",
    layout="wide"
)

# Recupera la query string
query_params = st.query_params
param_notebook_id = query_params.get("notebook_id", [None])[0]

# Salva in session_state se esiste
if param_notebook_id:
    st.session_state.current_notebook_id = param_notebook_id
    # opzionale: titolo se vuoi salvarlo
    st.session_state.current_notebook_title = st.session_state.get("current_notebook_title", "Notebook")

# Recupera sempre da session_state
notebook_id = st.session_state.get("current_notebook_id")
notebook_title = st.session_state.get("current_notebook_title", "Notebook")

if notebook_id:
    st.header(f"📓 Notebook: {notebook_id}")  #todo: retrieve_name
else:
    st.warning("Nessun notebook selezionato.")

# --- Inizializzazione chat manager ---
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager(user_id="test_user")

chat_manager: ChatManager = st.session_state.chat_manager

# --- Layout a tre colonne ---
col_docs, col_chat, col_tools = st.columns([1.2, 2, 1.2])

# ==========================
# 📚 COLONNA DOCUMENTI (SINISTRA)
# ==========================
with col_docs:
    st.header("📁 Documenti")
    uploaded_file = st.file_uploader("Carica documento PDF", type=["pdf"])
    if uploaded_file:
        save_dir = os.path.join("../../docs/")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        chat_manager.add_document(save_path)
        st.success(f"Documento '{uploaded_file.name}' aggiunto!")

    st.subheader("Documenti caricati")
    documents = chat_manager.list_documents()

    if not documents:
        st.info("Nessun documento caricato.")
    else:
        for doc in documents:
            doc_name = doc.metadata.get("source", "Senza nome")
            with st.container(border=True):
                st.write(f"📄 **{doc_name}**")
                if st.button(f"Elimina '{doc_name}'", key=f"del_{doc_name}"):
                    success = chat_manager.delete_document(doc_name)
                    if success:
                        st.success(f"Documento '{doc_name}' eliminato!")
                        st.rerun()
                    else:
                        st.error(f"Errore nell'eliminazione di '{doc_name}'")

# ==========================
# 💬 COLONNA CHAT (CENTRO)
# ==========================
with col_chat:

    # --- CSS compatto con altezza ridotta ---
    st.markdown(
        """
        <style>
        /* Contenitore scrollabile per i messaggi */
        .chat-container {
            height: 40vh;  /* Ridotto da 60vh a 40vh */
            overflow-y: auto;
            background-color: #f9f9f9;
            padding: 0.8rem;
            border-radius: 0.5rem;
            border: 1px solid #ddd;
        }

        /* Barra di input fissa in fondo */
        .chat-input-container {
            position: fixed;
            bottom: 1.2rem;
            left: 26%;   /* Adatta alla tua griglia Streamlit */
            width: 48%;
            background: white;
            padding: 0.6rem;
            border-top: 1px solid #ddd;
            z-index: 10;
            box-shadow: 0 -2px 6px rgba(0,0,0,0.05);
        }

        /* Messaggi compatti */
        .chat-bubble {
            padding: 0.5rem 0.7rem;
            border-radius: 0.5rem;
            margin-bottom: 0.4rem;
            word-wrap: break-word;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Stato della chat ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Area messaggi (ridotta) ---
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            color = "#DCF8C6" if msg["role"] == "user" else "#E8E8E8"
            label = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(
                f"""
                <div class="chat-bubble" style="background-color:{color}">
                    <strong>{label}</strong> {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Input fisso in basso ---
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_input = st.text_input("Scrivi la tua domanda:", key="chat_input", label_visibility="collapsed")
    send_button = st.button("Invia", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Logica invio messaggi ---
    if send_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        if chat_manager.is_ready():
            response = chat_manager.execute_rag_pipeline(user_input)
            if "error" in response:
                st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Errore: {response['error']}"})
            else:
                ai_reply = response.get("ai_response", "Nessuna risposta.")
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "⚠️ Il sistema non è pronto!"})
        st.rerun()

# ==========================
# 🧩 COLONNA TOOLS (DESTRA)
# ==========================
with col_tools:
    # --- Flashcard ---
    st.subheader("📘 Flashcard")

    flashcard_container = st.container()  # Placeholder dinamico

    flashcards = getattr(chat_manager, "list_flashcards", lambda: [])()
    with flashcard_container:
        if flashcards:
            for f in flashcards:
                with st.expander(f"🗂️ {f.get('title', 'Senza titolo')}"):
                    st.markdown(f"**Domanda:** {f.get('question', '—')}")
                    st.markdown(f"**Risposta:** {f.get('answer', '—')}")
        else:
            st.info("Nessuna flashcard disponibile.")

    st.divider()

    # --- Quiz ---
    st.subheader("🧠 Quiz")

    quiz_container = st.container()  # Placeholder dinamico

    quizzes = getattr(chat_manager, "list_quizzes", lambda: [])()
    with quiz_container:
        if quizzes:
            for q in quizzes:
                with st.expander(f"🧾 {q.get('title', 'Quiz senza titolo')}"):
                    questions = q.get("questions", [])
                    for i, ques in enumerate(questions, start=1):
                        st.markdown(f"**Domanda {i}:** {ques.get('question', '—')}")
                        st.markdown(f"• Risposta corretta: {ques.get('answer', '—')}")
        else:
            st.info("Nessun quiz disponibile.")

