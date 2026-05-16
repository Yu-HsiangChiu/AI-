import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv


st.set_page_config(page_title="AI 學術文獻智能問答系統", page_icon="🤖", layout="centered")
st.title("🤖 AI 學術文獻智能問答系統")
st.caption("Hugging Face Embedding + Gemini")

# ==========================================
# 初始化設定 (使用 Streamlit 的 cache 避免每次對話都重新載入)
# ==========================================

load_dotenv() # 自動抓 .env 檔案裡的API KEY

@st.cache_resource
def init_rag_system():
    """初始化向量資料庫與 LLM"""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    if not os.path.exists("輸入檔名"):
        return None, None
        
    loader = PyPDFLoader("輸入檔名")
    docs = loader.load()
    

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)
    
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    

    retriever = vectorstore.as_retriever(
        search_type="mmr", 
        search_kwargs={"k": 15, "fetch_k": 30}
    )
    
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)
    
    return retriever, llm

# 執行初始化
retriever, llm = init_rag_system()

if retriever is None:
    st.error("找不到 'pdf'，請確認檔案已放入專案資料夾中！")
    st.stop()

# ==========================================
# 記憶體管理
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # 給 LangChain 看的 Message 物件
if "ui_messages" not in st.session_state:
    st.session_state.ui_messages = [{"role": "assistant", "content": "我已經讀完這篇論文了，有什麼想問的嗎？"}] 

# ==========================================
# 渲染網頁歷史訊息
# ==========================================
for msg in st.session_state.ui_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ==========================================
# 使用者輸入框
# ==========================================
if user_query := st.chat_input("請輸入問題..."):
    
    # 1. 在網頁上顯示使用者的問題
    st.session_state.ui_messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
        
    # 2. 啟動 AI 檢索與生成回答
    with st.chat_message("assistant"):
        with st.spinner("正在論文中搜尋答案..."):
            try:
                # A. 檢索最相關的文獻段落
                relevant_docs = retriever.invoke(user_query)
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
                
                # B. 組織帶有上下文與歷史紀錄的 Prompt
                history_str = ""
                for msg in st.session_state.chat_history[-4:]: # 只取最近4輪對話當記憶，避免過度使用流量
                    role = "User" if isinstance(msg, HumanMessage) else "AI"
                    history_str += f"{role}: {msg.content}\n"
                
                prompt = f"""""請你扮演一個的論文專屬 AI 幫手，你的任務是幫助使用者快速且正確地理解這篇論文的核心技術與研究成果。

請嚴格遵守以下對話規則：
1. 【人設與語氣】：保持專業、友善、有耐心。回答時要有邏輯，多善用「條列式」或「步驟化」來解釋複雜的架構。
2. 【絕對誠實】：你的所有回答『必須』完全基於文章內的資料。如果使用者的問題超出了資料的範圍，請誠實且有禮貌地回答：「關於這個問題，在目前的論文段落中沒有特別提及」，絕對不能自己捏造數據或延伸瞎掰。
3. 【主動引導】：在解釋完一個複雜概念後，可以視情況用一句話引導使用者繼續發問（例如：「需要我進一步解釋 Grad-CAM 的運作原理嗎？」）。

如果你在參考資料中找不到答案，請誠實地說你不知道。

【對話歷史】:
{history_str}

【參考資料】:
{context}

【當前問題】:
{user_query}

請給出專業且結構清晰的回答。
"""
                ai_response = llm.invoke(prompt)
                answer = ai_response.content
                
                st.write(answer)
                
                st.session_state.ui_messages.append({"role": "assistant", "content": answer})
                st.session_state.chat_history.extend([
                    HumanMessage(content=user_query),
                    AIMessage(content=answer)
                ])
                
            except Exception as e:
                st.error(f"發生錯誤: {e}")