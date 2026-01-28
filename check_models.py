#check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Lỗi: Không tìm thấy GOOGLE_API_KEY trong file .env")
    print("Vui lòng tạo file .env với nội dung:")
    print("GOOGLE_API_KEY=your_api_key_here")
    exit(1)

genai.configure(api_key=api_key)

print("=" * 60)
print("📋 DANH SÁCH MODELS GEMINI KHẢ DỤNG")
print("=" * 60)

models_found = False

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        models_found = True
        print(f"\n✅ Model: {m.name}")
        print(f"   Display name: {m.display_name}")
        print(f"   Input token limit: {m.input_token_limit}")
        print(f"   Output token limit: {m.output_token_limit}")

if not models_found:
    print("\n⚠️ Không tìm thấy model nào hỗ trợ generateContent")
    print("Kiểm tra lại API key của bạn.")

print("\n" + "=" * 60)
print("💡 KHUYẾN NGHỊ: Dùng model có tên chứa 'flash' hoặc 'pro'")
print("=" * 60)