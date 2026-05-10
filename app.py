import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

st.set_page_config(page_title="React Interview Bot", layout="centered")
st.title("🤖 React Expert Interview Bot")

@st.cache_resource
def init_bot():
    if not os.path.exists("react.pdf"):
        st.error("Missing react.pdf in the project folder!")
        st.stop()
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    loader = PyPDFLoader("react.pdf")
    data = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(data)
    
    # Local embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(docs, embeddings)
    return llm, vector_db.as_retriever()

llm, retriever = init_bot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Memory-aware prompt
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a React expert. Use the context to answer.\n\nContext: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | qa_prompt
    | llm
    | StrOutputParser()
)

# UI Logic
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

if prompt := st.chat_input("Ask a React question..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 1. Retrieve the actual document objects
    docs = retriever.invoke(prompt)
    
    # 2. Run the chain to get the text answer
    response = rag_chain.invoke({
        "context": docs,
        "chat_history": st.session_state.chat_history,
        "input": prompt
    })
    
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # 3. Display the sources in an expander
        with st.expander("View Sources"):
            for i, doc in enumerate(docs):
                page_num = doc.metadata.get("page", "Unknown")
                # Showing a small snippet of the source text
                st.write(f"**Source {i+1} (Page {page_num + 1}):**")
                st.caption(f"{doc.page_content[:200]}...")

    # Save History
    st.session_state.chat_history.append(("human", prompt))
    st.session_state.chat_history.append(("ai", response))