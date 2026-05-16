import os
import google.generativeai as genai

def list_available_gemini_models():
    print("==================================================")
    print("   🤖 Gemini 可用模型與 ChatGoogleGenerativeAI 名稱查詢工具")
    print("==================================================")
    
    # 讓使用者輸入 API Key
    api_key = input("請輸入您的 Google API Key: ").strip()
    
    if not api_key:
        print("\n❌ 錯誤：API Key 不能為空！")
        return

    try:
        # 設定 API Key
        genai.configure(api_key=api_key)
        
        print("\n⏳ 正在向 Google 伺服器查詢可用模型列表...")
        models = genai.list_models()
        
        # 過濾出支援文字生成的模型 (generateContent)
        chat_models = [
            m for m in models 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        if not chat_models:
            print("\n找不到任何支援文字生成的 Gemini 模型。")
            return
            
        print(f"\n成功找到 {len(chat_models)} 個可用的文字生成模型！")
        
        # 畫出美觀的表格線條
        print(f"{'顯示名稱 (Display Name)':<35} | {'【MODEL NAME】(寫進Demo中的ChatGoogleGenerativeAI)'}")
        print("-" * 85)
        
        for model in chat_models:
            # model.name 通常會是 "models/gemini-2.5-flash" 這樣的格式
            print(f"{model.display_name:<35} | {model.name}")
            
        
    except Exception as e:
        print(f"\n❌ 查詢失敗！請檢查您的 API Key 是否正確或網路是否連通。")
        print(f"錯誤訊息: {e}")

if __name__ == "__main__":
    list_available_gemini_models()