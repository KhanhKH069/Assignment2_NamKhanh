#evaluate.py
import os
from dotenv import load_dotenv
from app import RAGPipeline

load_dotenv()

class RAGEvaluator:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        
    def evaluate_qa_pairs(self, qa_pairs):
        results = []
        for question, expected_keywords in qa_pairs:
            answer = self.pipeline.run(question)
            
            score = sum(1 for keyword in expected_keywords if keyword.lower() in answer.lower())
            max_score = len(expected_keywords)
            
            results.append({
                'question': question,
                'answer': answer,
                'score': score / max_score if max_score > 0 else 0,
                'keywords_found': score,
                'total_keywords': max_score
            })
        
        return results

if __name__ == "__main__":
    pipeline = RAGPipeline(data_path="data/input.txt")
    evaluator = RAGEvaluator(pipeline)
    
    # Câu hỏi test dựa trên file Câu_hỏi_mẫu.xlsx
    qa_test_set = [
        # Câu hỏi DỄ
        ("Các hạng mục trong màn hình quản lý người dùng?", 
         ["STT", "Mã cán bộ", "Tên cán bộ", "Email", "Đơn vị", "Phòng ban", "Phân nhóm"]),
        
        ("Các hạng mục trong màn hình Danh mục nhóm định giá?",
         ["STT", "Trung tâm định giá", "Mã đơn vị", "Mã nhóm", "Tên nhóm", "Ghi chú", "Điều kiện", "Trạng thái"]),
        
        ("Các hạng mục trong màn hình Quản lý đường phố?",
         ["STT", "Mã Đường", "Tên Đường", "Quận", "Huyện", "Trạng thái"]),
        
        ("Các hạng mục trong màn hình Thêm mới/Chỉnh sửa nhóm định giá?",
         ["Trung tâm định giá", "Mã nhóm", "Tên nhóm", "Điều kiện", "Thành viên"]),
        
        # Câu hỏi TRUNG BÌNH
        ("Luồng thực hiện của nghiệp vụ Thêm mới/Chỉnh sửa nhóm định giá?",
         ["Khởi tạo", "Tìm kiếm", "Thêm mới", "Lưu", "Cập nhật"]),
        
        ("Luồng thực hiện của nghiệp vụ Quản lý đường phố?",
         ["Khởi tạo", "Tìm kiếm", "Tab", "Thêm mới", "Xuất Excel"]),
        
        ("Luồng thực hiện của nghiệp vụ Quản lý người dùng?",
         ["Khởi tạo", "Nhập tiêu chí", "Tìm kiếm", "Hiển thị", "Danh sách"]),
        
        # Câu hỏi KHÓ
        ("Luồng thực hiện của nghiệp vụ Gửi phê duyệt, phê duyệt, từ chối cuộc tranh chấp",
         ["gửi phê duyệt", "phê duyệt", "từ chối", "email", "trạng thái"]),
        
        ("Luồng nghiệp vụ tổng quan của Tính năng quản lý tranh chấp",
         ["tạo mới", "gửi duyệt", "phê duyệt", "từ chối", "luồng", "trạng thái"]),
        
        ("So sánh luồng nghiệp vụ \"Danh mục Nhóm định giá\" và \"Thêm mới/Chỉnh sửa Nhóm định giá\"",
         ["Danh mục", "Thêm mới", "Chỉnh sửa", "khác nhau", "giống nhau", "luồng"])
    ]
    
    results = evaluator.evaluate_qa_pairs(qa_test_set)
    
    print("\n" + "=" * 80)
    print("KẾT QUẢ ĐÁNH GIÁ RAG PIPELINE - HỆ THỐNG QUẢN LÝ NGHIỆP VỤ")
    print("=" * 80 + "\n")
    
    total_score = 0
    for idx, result in enumerate(results, 1):
        print(f"Câu {idx}: {result['question']}")
        print(f"Trả lời: {result['answer'][:200]}...")
        print(f"Điểm: {result['score']:.2%} ({result['keywords_found']}/{result['total_keywords']} keywords)")
        print("-" * 80)
        total_score += result['score']
    
    avg_score = total_score / len(results)
    print(f"\n✅ ĐIỂM TRUNG BÌNH: {avg_score:.2%}")
    
    if avg_score >= 0.8:
        print("🎉 Xuất sắc! Pipeline hoạt động rất tốt.")
    elif avg_score >= 0.6:
        print("👍 Tốt! Pipeline hoạt động ổn định.")
    else:
        print("⚠️ Cần cải thiện! Xem xét điều chỉnh parameters.")