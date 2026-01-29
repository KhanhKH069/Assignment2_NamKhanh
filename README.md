# Readme.md
# RAG Pipeline - Hệ thống Tra cứu Nghiệp vụ

Hệ thống trả lời câu hỏi tự động về Quản lý Nghiệp vụ sử dụng RAG (Retrieval-Augmented Generation) với Gemini 2.5 Flash.

## 🚀 Tính năng

- ✅ Chunking thông minh với RecursiveCharacterTextSplitter (tối ưu cho tài liệu dài)
- ✅ Vietnamese-specific Embedding (BiEncoder)
- ✅ Vector Database với ChromaDB
- ✅ LLM Generation với Gemini 2.5 Flash (MIỄN PHÍ)
- ✅ Chain-of-Thought Prompting
- ✅ Streamlit UI đẹp với câu hỏi mẫu theo chủ đề

## 📚 Phạm vi tài liệu

Hệ thống hỗ trợ tra cứu 4 module chính:

1. **Quản lý người dùng**: Tìm kiếm, phân nhóm, xuất Excel
2. **Danh mục nhóm định giá**: Thêm/sửa/xóa, điều kiện, thành viên
3. **Quản lý đường/phố**: Tìm kiếm, nhập Excel, rule nghiệp vụ
4. **Quản lý tranh chấp**: Tạo mới, gửi phê duyệt, chuyển đơn vị

## 📦 Cài đặt

### 1. Clone repository

```bash
git clone <your-repo-url>
cd Assignment2_NamKhanh
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Cấu hình API Key

Tạo file `.env` và thêm:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Lấy API key tại: https://makersuite.google.com/app/apikey

## 🎯 Sử dụng

### Chế độ Terminal

```bash
python app.py
```

### Chế độ Web UI (Streamlit) - Khuyên dùng

```bash
streamlit run streamlit_app.py
```

### Đánh giá Pipeline

```bash
python evaluate.py
```

## 📊 Kiến trúc hệ thống

```
Input Documents → Chunking (1200 chars) → Embedding → VectorDB
                                                        ↓
User Query → Embedding → Retrieval (k=7) → LLM → Answer
```

## 🛠️ Tech Stack

| Component | Technology | Lý do lựa chọn |
|-----------|-----------|----------------|
| LLM | Gemini 2.5 Flash | MIỄN PHÍ, context 1M tokens |
| Chunking | RecursiveCharacterTextSplitter | Giữ nguyên ngữ nghĩa |
| Embedding | Vietnamese-BiEncoder | Tối ưu cho tiếng Việt |
| VectorDB | ChromaDB | Open-source, dễ setup |

## 📁 Cấu trúc dự án

```
Assignment2_NamKhanh/
├── data/
│   └── input.txt              # Tài liệu nghiệp vụ (hoàn chỉnh)
├── chroma_db/                 # Vector database (tự động tạo)
├── app.py                     # RAG Pipeline chính
├── streamlit_app.py           # Web UI
├── evaluate.py                # Đánh giá pipeline
├── check_models.py            # Kiểm tra Gemini models
├── requirements.txt           # Thư viện
├── .env                       # API keys
└── README.md                  # Hướng dẫn
```

## 🧪 Ví dụ câu hỏi

### Quản lý người dùng
```
1. Các hạng mục trong màn hình quản lý người dùng?
2. Luồng thực hiện của nghiệp vụ Quản lý người dùng?
3. Người dùng có thể tìm kiếm theo những tiêu chí nào?
```

### Danh mục nhóm định giá
```
1. Các hạng mục trong màn hình Danh mục nhóm định giá?
2. Luồng thực hiện của nghiệp vụ Thêm mới/Chỉnh sửa nhóm định giá?
3. Rule nghiệp vụ về dữ liệu hiển thị trong Danh mục nhóm định giá?
```

### Quản lý đường/phố
```
1. Các hạng mục trong màn hình Quản lý đường phố?
2. Luồng thực hiện của nghiệp vụ Quản lý đường phố?
3. Rule nghiệp vụ về tìm kiếm và dữ liệu hiển thị trong Đường/Phố?
```

### Quản lý tranh chấp
```
1. Luồng thực hiện của nghiệp vụ Gửi phê duyệt, phê duyệt, từ chối cuộc tranh chấp
2. Luồng nghiệp vụ tổng quan của Tính năng quản lý tranh chấp
3. So sánh luồng nghiệp vụ "Danh mục Nhóm định giá" và "Thêm mới/Chỉnh sửa Nhóm định giá"
```

## 🐛 Xử lý lỗi

### Lỗi: "No API key found"
```bash
# Kiểm tra file .env có đúng format
GOOGLE_API_KEY=AIza...
```

### Lỗi: "ChromaDB error"
```bash
# Xóa database và chạy lại
rm -rf chroma_db
python app.py
```

### Lỗi: "Model not found"
```bash
# Kiểm tra model available
python check_models.py
```

## 📝 Tùy chỉnh

### Thay đổi số lượng chunks retrieve
Trong `app.py`, sửa:
```python
search_kwargs={"k": 7}  # Tăng/giảm số này
```

### Thay đổi độ dài chunks
Trong `app.py`, sửa:
```python
chunk_size=1200,      # Tăng/giảm kích thước chunk
chunk_overlap=300,    # Tăng/giảm overlap
```

### Thay đổi temperature
Trong Streamlit UI, dùng slider "Temperature" (0.0 - 1.0)

## 🎯 Độ chính xác

Dựa trên evaluate.py với câu hỏi test:
- **Mục tiêu**: ≥ 80% keyword match
- **Thời gian phản hồi**: < 3s/câu hỏi

## 👨‍💻 Tác giả

**[Tên của bạn]**
- MSSV: [MSSV]
- Email: [Email]

## 📄 License

MIT License