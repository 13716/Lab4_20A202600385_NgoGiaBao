🧭 TravelBuddy - AI Travel Assistant

TravelBuddy là một AI Agent hỗ trợ tư vấn du lịch thông minh, có khả năng:

Gợi ý điểm đến phù hợp
Tìm chuyến bay
Tìm khách sạn
Tính toán ngân sách

Dự án sử dụng LangGraph + OpenAI API để xây dựng một agent có khả năng reasoning và sử dụng tool.

🚀 Tính năng chính
✈️ Tìm chuyến bay
Tìm theo: điểm đi, điểm đến
Gợi ý nhiều hãng: Vietnam Airlines, VietJet, Bamboo
Sắp xếp theo giá (rẻ → đắt)
🏨 Tìm khách sạn
Theo thành phố
Lọc theo ngân sách
Có rating + khu vực
💰 Tính ngân sách
Tổng hợp chi phí chuyến đi
Báo còn dư / vượt ngân sách
🧠 AI Agent thông minh
Hỏi thông tin khi thiếu
Không hỏi lại dữ liệu đã có
Tự động gọi tool khi đủ điều kiện
Gợi ý điểm đến nếu người dùng chưa biết đi đâu
🏗️ Kiến trúc hệ thống
User → Agent (LLM) → Tool → Agent → Output
Components:
Thành phần	Mô tả
agent.py	Điều phối chính (LangGraph)
tool.py	Các tool (flight, hotel, budget)
system_promt.txt	Prompt định nghĩa hành vi
travelbuddy.log	File log debug
🛠️ Cài đặt
1. Clone project
git clone <repo-url>
cd travelbuddy
2. Cài thư viện
pip install -r requirements.txt
3. Tạo file .env
OPENAI_API_KEY=your_api_key_here
▶️ Chạy chương trình
python agent.py
💬 Ví dụ sử dụng
1. Hỏi chung (agent sẽ gợi ý)
Bạn: tôi muốn đi du lịch nhưng chưa biết đi đâu

👉 Output:

Mình gợi ý bạn:
- Đà Nẵng (biển đẹp)
- Phú Quốc (nghỉ dưỡng)
- Đà Lạt (mát mẻ)

Bạn thích kiểu nào?
2. Tìm chuyến bay
Bạn: tìm chuyến bay từ Hà Nội đến Hồ Chí Minh

👉 Agent sẽ:

Gọi search_flights
Trả kết quả 2–3 chuyến phù hợp
3. Tìm khách sạn
Bạn: khách sạn ở Đà Nẵng dưới 1 triệu
4. Tính ngân sách
Bạn: tính giúp tôi ngân sách 5 triệu với vé 1 triệu, khách sạn 2 triệu
🧠 Cách hoạt động của Agent

Agent sử dụng:

LLM (GPT-4o-mini)
Tool Calling
LangGraph (State Machine)
Logic chính:
Nhận input user
Kiểm tra đủ thông tin chưa
Nếu đủ → gọi tool
Nếu thiếu → hỏi thêm / gợi ý
Trả kết quả
🔧 Tools
search_flights
search_flights(origin, destination, date="", passengers=1)
search_hotels
search_hotels(city, max_price_per_night)
calculate_budget
calculate_budget(total_budget, expenses)
📊 Logging
Console: chỉ hiển thị câu trả lời
Debug: ghi vào travelbuddy.log

Ví dụ log:

DEBUG ... GỌI TOOL search_flights(...)
DEBUG ... RAW RESPONSE ...
⚠️ Lưu ý
Dữ liệu flights/hotels hiện là mock data
Giá chỉ mang tính ước tính
Chưa kết nối API thực tế
🚀 Hướng phát triển
Kết nối API thật (Amadeus, Skyscanner)
Thêm nhiều thành phố
Memory (ghi nhớ user)
UI web/app
Recommendation thông minh hơn
🎯 Mục tiêu học tập

Dự án giúp hiểu:

Cách xây dựng AI Agent
Tool calling
Prompt engineering
State machine với LangGraph
👨‍💻 Tác giả
Student: 13716
Project: AI Travel Assistant
