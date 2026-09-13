import json
from typing import Dict, Any

# ==============================================================================
# 1. TOOL SCHEMA DEFINITIONS (Dành cho LLM hiểu chức năng của Tool)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "query_jd",
        "description": "Tra cứu thông tin chi tiết và tiêu chí bắt buộc của một vị trí tuyển dụng (Job Description).",
        "parameters": {
            "type": "object",
            "properties": {
                "position": {
                    "type": "string",
                    "description": "Tên vị trí cần tra cứu (ví dụ: 'AI Engineer', 'Backend Developer', 'Data Scientist')"
                }
            },
            "required": ["position"]
        }
    },
    {
        "name": "read_cv",
        "description": "Đọc và trích xuất nội dung từ file CV (PDF/Doc) của ứng viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Đường dẫn hoặc tên file CV (ví dụ: 'tran_van_b.pdf', 'le_van_c.pdf')"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "schedule_interview",
        "description": "Lên lịch phỏng vấn với ứng viên sau khi đã đánh giá Đạt yêu cầu.",
        "parameters": {
            "type": "object",
            "properties": {
                "candidate_name": {
                    "type": "string",
                    "description": "Tên ứng viên (ví dụ: 'Trần Văn B')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                "position": {
                    "type": "string",
                    "description": "Vị trí ứng tuyển (ví dụ: 'Backend Developer')"
                }
            },
            "required": ["candidate_name", "datetime_str", "position"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_JD_DB = {
    "AI ENGINEER": {
        "position": "AI Engineer",
        "required_skills": ["Python", "PyTorch", "TensorFlow", "Audio Processing"],
        "experience": "2+ years",
        "status": "OPEN"
    },
    "BACKEND DEVELOPER": {
        "position": "Backend Developer",
        "required_skills": ["Java", "Spring Boot", "Microservices", "PostgreSQL", "Redis"],
        "experience": "3+ years",
        "status": "OPEN"
    },
    "DATA SCIENTIST": {
        "position": "Data Scientist",
        "required_skills": ["Python", "Machine Learning", "SQL", "Statistics"],
        "experience": "1+ years",
        "status": "OPEN"
    }
}

MOCK_CV_STORAGE = {
    "tran_van_b.pdf": "Họ tên: Trần Văn B. Vị trí ứng tuyển: Backend Developer. Kinh nghiệm: 4 năm làm Java, Spring Boot, thiết kế hệ thống Microservices, tối ưu CSDL PostgreSQL và sử dụng Redis caching tại công ty TechVN.",
    "le_van_c.pdf": "Họ tên: Lê Văn C. Vị trí ứng tuyển: Data Scientist. Kinh nghiệm: 2 năm làm Kế toán trưởng, chuyên sử dụng phần mềm kế toán và Excel, không biết lập trình Python hay SQL.",
    "nguyen_van_a.pdf": "Họ tên: Nguyễn Văn A. Vị trí ứng tuyển: Data Scientist. Kinh nghiệm: 3 năm làm Data Scientist, chuyên xử lý dữ liệu với SQL và build model bằng Python."
}

def execute_query_jd(position: str) -> str:
    """Thực thi tra cứu Job Description"""
    jd = MOCK_JD_DB.get(position.strip().upper())
    if jd:
        return json.dumps({"status": "SUCCESS", "data": jd}, ensure_ascii=False)
    return json.dumps({"status": "NOT_FOUND", "message": f"Không tìm thấy JD cho vị trí '{position}'"}, ensure_ascii=False)

def execute_read_cv(file_path: str) -> str:
    """Thực thi giả lập việc đọc file CV (PDF/Doc)"""
    content = MOCK_CV_STORAGE.get(file_path.strip().lower())
    if content:
        return json.dumps({"status": "SUCCESS", "content": content}, ensure_ascii=False)
    return json.dumps({"status": "FILE_ERROR", "message": f"Lỗi đọc file: '{file_path}' không tồn tại hoặc bị hỏng!"}, ensure_ascii=False)

def execute_schedule_interview(candidate_name: str, datetime_str: str, position: str) -> str:
    """Thực thi việc đặt lịch phỏng vấn"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"INT-{candidate_name.replace(' ', '')}-99",
        "candidate": candidate_name,
        "datetime": datetime_str,
        "position": position,
        "message": f"Hệ thống đã tự động gửi email đặt lịch phỏng vấn cho ứng viên {candidate_name} (Vị trí {position}) vào lúc {datetime_str}."
    }, ensure_ascii=False)

# Router gọi tool thực tế
TOOL_ROUTER = {
    "query_jd": execute_query_jd,
    "read_cv": execute_read_cv,
    "schedule_interview": execute_schedule_interview,
    "schedule_appointment": execute_schedule_interview # Alias tương thích với các tool call cũ (nếu có)
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại trong hệ thống!"}, ensure_ascii=False)
