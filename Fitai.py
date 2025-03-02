import streamlit as st
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.documents import Document
import re

# Styling
st.markdown("""
<style>
    /* Main background and text */
    .main {
        background-color: #f5f5f5; /* Soft, elegant cream */
        color: #2c3e50; /* Deep navy for classy contrast */
        font-family: 'Arial', sans-serif; /* Clean, modern font */
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #34495e; /* Rich slate blue for sophistication */
        border-radius: 10px; /* Rounded corners for polish */
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    }

    /* Chat window styling */
    .stChatMessage {
        background-color: #ecf0f1; /* Light gray for messages */
        border-radius: 12px; /* Rounded for friendliness */
        padding: 12px;
        margin: 5px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stChatMessage.user {
        background-color: #3498db; /* Blue for user messages, Grok-inspired */
        color: #ffffff;
    }
    .stChatMessage.assistant {
        background-color: #2ecc71; /* Vibrant green for assistant, witty and fun */
        color: #ffffff;
    }
    .stChatMessage.assistant img {
        animation: bounce 2s infinite; /* Playful animation for assistant icon */
    }

    /* Input field (chat input) */
    .stChatInput {
        background-color: #ecf0f1; /* Light gray for input */
        border: 2px solid #3498db; /* Bright blue accent */
        border-radius: 8px;
        padding: 10px;
        transition: border-color 0.3s ease; /* Smooth focus effect */
    }
    .stChatInput:focus {
        border-color: #e74c3c; /* Playful red for focus */
        outline: none;
    }
    .stChatInput::placeholder {
        color: #7f8c8d; /* Muted gray for placeholder, witty touch */
        font-style: italic;
    }

    /* Buttons (send button) */
    .stButton>button {
        background-color: #3498db; /* Bright blue for action */
        color: #ffffff;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #e74c3c; /* Playful red for hover, witty twist */
        cursor: pointer;
    }

    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #34495e; /* Matches sidebar */
        color: #ffffff !important;
        border: 2px solid #3498db; /* Blue accent */
        border-radius: 8px;
        padding: 8px;
    }
    .stSelectbox svg {
        fill: #ffffff !important; /* White dropdown arrow */
    }
    .stSelectbox option {
        background-color: #34495e !important;
        color: #ffffff !important;
    }
    div[role="listbox"] div {
        background-color: #34495e !important;
        color: #ffffff !important;
        border-radius: 8px;
    }

    /* Title styling */
    h1 {
        color: #e74c3c; /* Playful red for title, witty and classy */
        font-family: 'Georgia', serif; /* Elegant font */
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    }

    /* Sidebar content */
    .sidebar h1 {
        color: #e74c3c; /* Red for header, matching title */
        font-family: 'Georgia', serif;
    }
    .sidebar .stMarkdown {
        color: #ffffff; /* White text for readability */
    }

    /* Animation for wit */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    /* Multitasking tabs (custom CSS for tabs if needed) */
    .stTabs {
        background-color: #34495e;
        border-radius: 8px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #34495e;
        color: #ffffff;
        border: none;
        padding: 8px 16px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e74c3c; /* Red for hover, witty */
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: none;
    }

    /* Caption or footer */
    .stCaption {
        color: #7f8c8d; /* Muted gray for captions */
        font-style: italic; /* Classy touch */
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎩 FitSmart Command Center")
    selected_model = st.selectbox(
        "Choose Your Fitness Guru",
        ["Llama 3.2", "deepseek-r1:3b"],
        index=0,
        help="Pick the brainpower behind your workout wisdom—witty and wise!"
    )
    st.divider()
    st.markdown("### Superpowers of FitSmart")
    st.markdown("""
    - 🏋️‍♂️ Workout Wizard
    - 🏃‍♂️ Sweat Session Savior
    - 🍎 Nutrition Ninja
    - 💡 Genius Moves Designer
    """)
    st.divider()
    st.markdown("Powered by [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/) ✨")



# Constants
PROMPT_TEMPLATE = """
You are an advanced AI-powered fitness assistant focused on providing personalized workout recommendations based on user profiles, fitness goals, and health conditions. Your primary goal is to refine workout suggestions step by step, ensuring that each recommendation is highly tailored to the user's needs and preferences.

Start by gathering essential user details, such as age, weight, fitness level, and specific goals.
For each input provided, ask follow-up questions to refine the workout plan and eliminate irrelevant routines.
Always prioritize tailoring workouts to individual needs, considering factors like health conditions (e.g., diabetes, hypertension) and lifestyle constraints.
If there is insufficient information, ask for clarification before generating a recommendation.
Ensure that each interaction leads to a more precise and optimized fitness plan, evolving as the user progresses.
At the end of the interaction, provide a personalized workout plan along with estimated calorie burn.
Recommend consulting a certified fitness expert or healthcare professional for personalized medical advice if needed.
Important: Avoid asking too many questions in a single interaction and ensure that after 3-4 exchanges, the conversation leads to an informed conclusion. Be more conversational and avoid third-person speech.

Chat History:
{chat_history}

New Query: {user_query}
Context: {document_context}
Answer:

Chat History:
{chat_history}

New Query: {user_query}
Context: {document_context}
Answer:
"""

EMBEDDING_MODEL = OllamaEmbeddings(model="llama3.2")
DOCUMENT_VECTOR_DB = InMemoryVectorStore(EMBEDDING_MODEL)
LANGUAGE_MODEL = OllamaLLM(model="llama3.2")

# Load knowledge base
def load_knowledge_base():
    with open("fitness_dataset.txt", "r", encoding="utf-8") as file:
        content = file.read()
    DOCUMENT_VECTOR_DB.add_documents([Document(page_content=content)])

load_knowledge_base()

def find_related_documents(query):
    return DOCUMENT_VECTOR_DB.similarity_search(query)

def generate_answer(user_query, context_documents, chat_history):
    context_text = "\n\n".join([doc.page_content for doc in context_documents])
    full_chat_history = "\n".join([f"User: {msg['user']}\nAssistant: {msg['assistant']}" for msg in chat_history])
    
    conversation_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    response_chain = conversation_prompt | LANGUAGE_MODEL
    response = response_chain.invoke({
        "user_query": user_query,
        "document_context": context_text,
        "chat_history": full_chat_history
    })
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    return response

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# UI
st.title("🦾 FitSmart: AI-Powered Fitness Assistant ⚡")
st.caption("💪🤖 Get personalized workout and nutrition guidance with AI")
st.markdown("---")

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant", avatar="🤖"):
        st.write(chat["assistant"])

# User input
user_input = st.chat_input("Ask anything about your fitness, workouts, or nutrition...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("🧠 Analyzing..."):
        relevant_docs = find_related_documents(user_input)
        ai_response = generate_answer(user_input, relevant_docs, st.session_state.chat_history)

    # Update chat history
    st.session_state.chat_history.append({"user": user_input, "assistant": ai_response})

    with st.chat_message("assistant", avatar="🤖"):
        st.write(ai_response)