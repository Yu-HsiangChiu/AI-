# 🤖 AI 學術文獻智能問答系統 (RAG-based Thesis Assistant)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?logo=google&logoColor=white)

本專案是一個基於 **檢索增強生成 (Retrieval-Augmented Generation, RAG)** 架構開發的學術文獻智能問答系統。主要應用於解析與探討「雙重可解釋性人工智慧架構於食物影像辨識與用藥安全」之碩士論文，提供流暢的互動式問答體驗。

## 💡 系統特色

* **混合式 RAG 架構 (Hybrid RAG)**：為解決雲端 API 頻繁呼叫的流量限制 (Rate Limits) 與潛在資安問題，本系統將 Embedding 抽離雲端，**全面改用 Hugging Face 本地端開源多語言模型**進行文獻向量化，大幅降低運行成本與延遲。
* **精準上下文檢索**：搭配 ChromaDB 向量資料庫，並優化切詞策略 (Chunking) 與檢索數量 (k-value)，確保 LLM 能掌握長篇學術論文的完整脈絡。
* **歷史記憶對話 (Memory)**：具備記憶對話能力，系統能根據上下文脈絡理解後續提問。
* **友善 UI 介面**：使用 Streamlit 打造直覺的對話視窗，快速上手測試。

## 🛠️ 技術使用

* **前端介面**：Streamlit
* **大語言模型 (LLM)**：Google Gemini API 
* **向量模型 (Embedding)**：Hugging Face (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` 本地運行)
* **向量資料庫**：ChromaDB
* **框架**：LangChain

## 📸 系統展示 (Demo)

> **<img width="1258" height="843" alt="DEMO" src="https://github.com/user-attachments/assets/adb15c75-6836-46d9-87f2-d3f79c572c7c" />**

## 🚀 使用流程 (Quick Start)
請依照以下步驟設定並啟動系統：
* **Step 1.** 設定 Gemini API Key : 開啟.env 檔案，輸入您的 Google Gemini API 金鑰
* **Step 2.** 挑選 Gemini 模型 : 在終端機執行 check_models.py，系統會列出您的 API Key 可使用的模型
* **Step 3.** 設定主程式 : 輸入要使用的Gemini model名稱，與要讀取的PDF檔名
* **Step 4.** 啟動系統 : 輸入streamlit run demo.py

## 🚀 快速啟動 (Quick Start)

### 1. 安裝環境依賴
請確保已安裝 Python 3.8 以上版本，並執行以下指令安裝所需套件：
```bash
pip install streamlit langchain langchain-community langchain-chroma langchain-google-genai langchain-huggingface langchain-text-splitters google-generativeai python-dotenv pypdf sentence-transformers
