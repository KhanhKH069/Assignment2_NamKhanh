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
    
    qa_test_set = [
        ("Chức năng quản lý người dùng là gì?", 
         ["tìm kiếm", "xuất Excel", "phân nhóm", "phân quyền"]),
        
        ("Điều kiện để thêm mới nhóm định giá là gì?",
         ["Trung tâm định giá", "Mã nhóm", "Tên nhóm", "Điều kiện", "Thành viên"]),
        
        ("Khi nào không thể xóa nhóm định giá?",
         ["hồ sơ đang xử lý", "không thể xoá", "kiểm tra"]),
        
        ("Rule nghiệp vụ khi nhập đường phố từ Excel là gì?",
         ["không dấu", "lowercase", "ràng buộc", "alias"]),
        
        ("Quy trình gửi phê duyệt cuộc tranh chấp như thế nào?",
         ["Chi nhánh", "Trụ sở chính", "người duyệt", "email"]),
        
        ("Trạng thái nào cho phép chỉnh sửa cuộc tranh chấp?",
         ["Tạo mới", "Từ chối duyệt", "Đã phê duyệt"]),
        
        ("Điều kiện vấn tin CIF khi tạo cuộc tranh chấp?",
         ["Họ và tên", "Chi nhánh quản lý", "KHCN", "KHDN"])
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