# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Bùi Việt Anh 
> **Mã Sinh Viên / Mã Học viên:** 2A202602611  
> **Chủ đề Lựa chọn:** Trợ lý Tuyển dụng & Sàng lọc CV

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Hệ thống cần thực hiện chuỗi suy luận rõ ràng: Đọc CV -> Trích xuất dữ liệu -> Tra cứu Job Description (JD) -> Đối chiếu -> Đánh giá Đạt/Trượt -> Xếp lịch. |
| **2. Tool Interaction** | 4 / 5 | Cần kết nối với nhiều công cụ ngoại vi: Trình đọc PDF/Doc, CSDL lưu trữ tiêu chí JD (MCP Server), API Email để gửi thông báo, và API Lịch để tìm slot trống. |
| **3. Dynamic Decision** | 4 / 5 | Hành động phụ thuộc chặt chẽ vào kết quả trước đó. Ví dụ: Nếu CV Đạt -> tìm lịch rảnh để mời phỏng vấn; Nếu Trượt -> gửi thư từ chối; Nếu lỗi đọc CV -> thử lại. |
| **4. Long Horizon Goal** | 4 / 5 | Agent phải duy trì mục tiêu "Hoàn tất quy trình sàng lọc và xếp lịch" xuyên suốt quá trình dài qua nhiều công cụ và bước kiểm tra, không chỉ là 1-2 thao tác hỏi đáp đơn giản. |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | *Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Ứng viên Nguyễn Văn A ứng tuyển vị trí Data Scientist đã đạt yêu cầu vòng hồ sơ. Hãy xếp lịch phỏng vấn cho ứng viên này vào lúc 14:00 chiều thứ Tư tuần này.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "read_cv",
    "arguments": {
      "file_path": "nguyen_van_a.pdf"
    },
    "observation": {
      "status": "SUCCESS",
      "content": "Họ tên: Nguyễn Văn A. Vị trí ứng tuyển: Data Scientist. Kinh nghiệm: 3 năm làm Data Scientist, chuyên xử lý dữ liệu với SQL và build model bằng Python."
    },
    "latency_ms": 4479.37
  },
  {
    "step": 2,
    "query": "Ứng viên Nguyễn Văn A ứng tuyển vị trí Data Scientist đã đạt yêu cầu vòng hồ sơ. Hãy xếp lịch phỏng vấn cho ứng viên này vào lúc 14:00 chiều thứ Tư tuần này.\n\n[Action]: Đã gọi tool read_cv\n[Observation]: {\"status\": \"SUCCESS\", \"content\": \"Họ tên: Nguyễn Văn A. Vị trí ứng tuyển: Data Scientist. Kinh nghiệm: 3 năm làm Data Scientist, chuyên xử lý dữ liệu với SQL và build model bằng Python.\"}\nHãy tiếp tục suy luận và ra quyết định.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "query_jd",
    "arguments": {
      "position": "Data Scientist"
    },
    "observation": {
      "status": "SUCCESS",
      "data": {
        "position": "Data Scientist",
        "required_skills": [
          "Python",
          "Machine Learning",
          "SQL",
          "Statistics"
        ],
        "experience": "1+ years",
        "status": "OPEN"
      }
    },
    "latency_ms": 4783.57
  },
  {
    "step": 3,
    "query": "Ứng viên Nguyễn Văn A ứng tuyển vị trí Data Scientist đã đạt yêu cầu vòng hồ sơ. Hãy xếp lịch phỏng vấn cho ứng viên này vào lúc 14:00 chiều thứ Tư tuần này.\n\n[Action]: Đã gọi tool read_cv\n[Observation]: {\"status\": \"SUCCESS\", \"content\": \"Họ tên: Nguyễn Văn A. Vị trí ứng tuyển: Data Scientist. Kinh nghiệm: 3 năm làm Data Scientist, chuyên xử lý dữ liệu với SQL và build model bằng Python.\"}\nHãy tiếp tục suy luận và ra quyết định.\n\n[Action]: Đã gọi tool query_jd\n[Observation]: {\"status\": \"SUCCESS\", \"data\": {\"position\": \"Data Scientist\", \"required_skills\": [\"Python\", \"Machine Learning\", \"SQL\", \"Statistics\"], \"experience\": \"1+ years\", \"status\": \"OPEN\"}}\nHãy tiếp tục suy luận và ra quyết định.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "schedule_interview",
    "arguments": {
      "datetime_str": "14:00 chiều thứ Tư tuần này",
      "candidate_name": "Nguyễn Văn A",
      "position": "Data Scientist"
    }
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [X] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 8 lượt.
- **Kết quả đẩy Repo nộp bài:** [X] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
