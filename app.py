#app.py
import os
import warnings
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

load_dotenv()

class RAGPipeline:
    def __init__(self, data_path):
        self.data_path = data_path
        self.vector_db_path = "./chroma_db"
        self.embedding_model_name = "bkai-foundation-models/vietnamese-bi-encoder"
        
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            temperature=0.3
        )

        print("🔄 Loading Embeddings Model (CPU)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

    def ingest_data(self):
        print(f"📂 Loading data from {self.data_path}...")
        loader = TextLoader(self.data_path, encoding='utf-8')
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=300,
            separators=["\n========================================\n", "\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"🧩 Split into {len(chunks)} chunks.")

        print("💽 Creating Vector Database...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.vector_db_path
        )
        return vectorstore

    def get_retriever(self, vectorstore):
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 7}
        )
        return retriever

    def build_chain(self, retriever):
        template = """Bạn là một trợ lý AI chuyên về Hệ thống Quản lý Nghiệp vụ. Hãy trả lời câu hỏi dựa trên tài liệu nghiệp vụ được cung cấp.
        
        Quy trình suy nghĩ (Chain-of-Thought):
        1. Phân tích câu hỏi để hiểu ý định người dùng
        2. Tìm kiếm thông tin liên quan trong tài liệu nghiệp vụ
        3. Tổng hợp thông tin và đưa ra câu trả lời chính xác, chi tiết bằng tiếng Việt
        4. Nếu có nhiều bước hoặc điều kiện, hãy liệt kê rõ ràng
        
        LƯU Ý QUAN TRỌNG:
        - Chỉ trả lời dựa trên thông tin có trong ngữ cảnh
        - Nếu không tìm thấy thông tin → nói rõ "Thông tin này không có trong tài liệu"
        - Trả lời ngắn gọn, súc tích nhưng đầy đủ
        - Sử dụng bullet points nếu có nhiều điểm

        Ngữ cảnh:
        {context}

        Câu hỏi: {question}

        Trả lời:"""

        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def run(self, query):
        if not os.path.exists(self.vector_db_path):
            print("⚠️ Vector DB not found. Ingesting data...")
            vectorstore = self.ingest_data()
        else:
            vectorstore = Chroma(
                persist_directory=self.vector_db_path, 
                embedding_function=self.embeddings
            )
        
        retriever = self.get_retriever(vectorstore)
        chain = self.build_chain(retriever)
        
        response = chain.invoke(query)
        return response

if __name__ == "__main__":
    input_file = "data/input.txt"
    if not os.path.exists(input_file):
        os.makedirs("data", exist_ok=True)
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("Hệ thống quản lý nghiệp vụ - Tài liệu hướng dẫn sử dụng.")
    
    pipeline = RAGPipeline(data_path=input_file)
    
    print("=" * 70)
    print("RAG PIPELINE - HỆ THỐNG TRẢ LỜI CÂU HỎI NGHIỆP VỤ")
    print("=" * 70)
    
    while True:
        user_query = input("\n📝 Nhập câu hỏi (gõ 'exit' để thoát): ")
        if user_query.lower() in ['exit', 'quit']:
            print("\n👋 Tạm biệt!")
            break
        
        try:
            print("\n🔍 Đang xử lý...")
            answer = pipeline.run(user_query)
            print(f"\n🤖 Trả lời:\n{answer}")
        except Exception as e:
            print(f"\n❌ Error: {e}")