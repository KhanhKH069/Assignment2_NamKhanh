#streamlit_app.py
import streamlit as st
import warnings
from app import RAGPipeline
import time

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="Hệ thống Tra cứu Nghiệp vụ",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Hệ thống Tra cứu Nghiệp vụ - RAG QA System")
st.markdown("**Hỗ trợ tra cứu thông tin về: Quản lý người dùng, Nhóm định giá, Đường/Phố, Tranh chấp**")

@st.cache_resource
def load_pipeline():
    return RAGPipeline(data_path="data/input.txt")

pipeline = load_pipeline()

st.sidebar.header("⚙️ Cài đặt")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
pipeline.llm.temperature = temperature

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Câu hỏi mẫu")

st.sidebar.markdown("**🔹 Quản lý người dùng:**")
if st.sidebar.button("Các hạng mục trong màn hình?"):
    st.session_state['question'] = "Các hạng mục trong màn hình quản lý người dùng?"

if st.sidebar.button("Luồng thực hiện nghiệp vụ?"):
    st.session_state['question'] = "Luồng thực hiện của nghiệp vụ Quản lý người dùng?"

if st.sidebar.button("Tiêu chí tìm kiếm người dùng?"):
    st.session_state['question'] = "Người dùng có thể tìm kiếm theo những tiêu chí nào?"

st.sidebar.markdown("**🔹 Nhóm định giá:**")
if st.sidebar.button("Hạng mục Danh mục nhóm định giá?"):
    st.session_state['question'] = "Các hạng mục trong màn hình Danh mục nhóm định giá?"

if st.sidebar.button("Luồng Thêm mới/Chỉnh sửa?"):
    st.session_state['question'] = "Luồng thực hiện của nghiệp vụ Thêm mới/Chỉnh sửa nhóm định giá?"

if st.sidebar.button("Rule nghiệp vụ nhóm định giá?"):
    st.session_state['question'] = "Rule nghiệp vụ về dữ liệu hiển thị trong Danh mục nhóm định giá?"

st.sidebar.markdown("**🔹 Đường/Phố:**")
if st.sidebar.button("Hạng mục Quản lý đường phố?"):
    st.session_state['question'] = "Các hạng mục trong màn hình Quản lý đường phố?"

if st.sidebar.button("Luồng nghiệp vụ đường phố?"):
    st.session_state['question'] = "Luồng thực hiện của nghiệp vụ Quản lý đường phố?"

st.sidebar.markdown("**🔹 Tranh chấp:**")
if st.sidebar.button("Luồng Gửi phê duyệt?"):
    st.session_state['question'] = "Luồng thực hiện của nghiệp vụ Gửi phê duyệt, phê duyệt, từ chối cuộc tranh chấp"

if st.sidebar.button("Tổng quan quản lý tranh chấp?"):
    st.session_state['question'] = "Luồng nghiệp vụ tổng quan của Tính năng quản lý tranh chấp"

if st.sidebar.button("So sánh Danh mục vs Thêm mới?"):
    st.session_state['question'] = "So sánh luồng nghiệp vụ \"Danh mục Nhóm định giá\" và \"Thêm mới/Chỉnh sửa Nhóm định giá\""

if 'history' not in st.session_state:
    st.session_state['history'] = []

col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input(
        "💬 Nhập câu hỏi của bạn:", 
        value=st.session_state.get('question', ''),
        placeholder="VD: Các hạng mục trong màn hình quản lý người dùng?"
    )

with col2:
    st.write("")
    st.write("")
    ask_button = st.button("🔍 Hỏi", type="primary", use_container_width=True)

if ask_button and question:
    with st.spinner("🤔 Đang tìm kiếm trong tài liệu nghiệp vụ..."):
        start_time = time.time()
        try:
            answer = pipeline.run(question)
            elapsed_time = time.time() - start_time
            
            st.session_state['history'].insert(0, {
                'question': question,
                'answer': answer,
                'time': elapsed_time
            })
            
            st.success("✅ Hoàn thành!")
            
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")

if st.session_state['history']:
    st.markdown("---")
    st.subheader("💬 Lịch sử tra cứu")
    
    for idx, item in enumerate(st.session_state['history']):
        with st.expander(f"Q{idx+1}: {item['question']}", expanded=(idx==0)):
            st.markdown(f"**🤖 Trả lời:** {item['answer']}")
            st.caption(f"⏱️ Thời gian xử lý: {item['time']:.2f}s")

if st.sidebar.button("🗑️ Xóa lịch sử"):
    st.session_state['history'] = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("""
**Tech Stack:**
- LLM: Gemini 2.5 Flash (FREE)
- Embedding: Vietnamese-BiEncoder
- Vector DB: ChromaDB
- Framework: LangChain

**Phạm vi tài liệu:**
✅ Quản lý người dùng
✅ Danh mục nhóm định giá
✅ Quản lý đường/phố
✅ Quản lý tranh chấp
""")