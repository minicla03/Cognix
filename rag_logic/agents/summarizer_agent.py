from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama


def summary_agent(conversation_history: list, language_hint="italian"):

    conv_text = "\n".join(
        f"{type(msg).__name__}: {msg.content}" if hasattr(msg, "content") else str(msg)
        for msg in conversation_history
    )

    prompt_summary = f"""
        "You are a chat summarization agent. "
        "Your task is to analyze the entire conversation history between the user and the assistant "
        "and produce a clear, concise summary capturing the essential information.\n\n"

        "Guidelines:\n"
        "- Write in {language_hint}.\n"
        "- Focus on the main topics discussed, the user’s goals, and any specific requests or constraints.\n"
        "- Omit greetings, filler phrases, or unrelated small talk.\n"
        "- Maintain a neutral and factual tone.\n"
        "- If the conversation includes technical explanations, summarize the key points without unnecessary detail.\n\n"

        "Your output should be a short paragraph (5–7 lines) that provides enough context "
        "for another model to understand what the conversation was about and continue it smoothly.\n\n"
    """

    messages = [
        SystemMessage(content=prompt_summary),
        HumanMessage(content=conv_text)
    ]

    llm = ChatOllama(model="llama3:latest", temperature=0.1, top_p=0.95, top_k=40)
    response = llm.invoke(messages)
    summary = response.content
    print(summary)
    return summary
