from langchain_core.tools import tool

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival":
"07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival":
"15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",       "departure": "08:30", "arrival":
"09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",    "departure": "11:00", "arrival":
"12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival":
"09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "10:00", "arrival":
"12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "16:00", "arrival":
"18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival":
"08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "07:30", "arrival":
"09:40", "price": 950_000,   "class": "economy"},
        {"airline": "Bamboo Airways",    "departure": "12:00", "arrival":
"14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival":
"20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival":
"10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "13:00", "arrival":
"14:20", "price": 780_000,   "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival":
"09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "15:00", "arrival":
"16:00", "price": 650_000,   "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",    "stars": 5, "price_per_night":
1_800_000, "area": "Mỹ Khê",      "rating": 4.5},
        {"name": "Sala Danang Beach",     "stars": 4, "price_per_night":
1_200_000, "area": "Mỹ Khê",      "rating": 4.3},
        {"name": "Fivitel Danang",        "stars": 3, "price_per_night":
650_000,   "area": "Sơn Trà",     "rating": 4.1},
        {"name": "Memory Hostel",         "stars": 2, "price_per_night":
250_000,   "area": "Hải Châu",    "rating": 4.6},
        {"name": "Christina's Homestay",  "stars": 2, "price_per_night":
350_000,   "area": "An Thượng",   "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",       "stars": 5, "price_per_night":
3_500_000, "area": "Bãi Dài",     "rating": 4.4},
        {"name": "Sol by Meliá",          "stars": 4, "price_per_night":
1_500_000, "area": "Bãi Trường",  "rating": 4.2},
        {"name": "Lahana Resort",         "stars": 3, "price_per_night":
800_000,   "area": "Dương Đông",  "rating": 4.0},
        {"name": "9Station Hostel",       "stars": 2, "price_per_night":
200_000,   "area": "Dương Đông",  "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",             "stars": 5, "price_per_night":
2_800_000, "area": "Quận 1",      "rating": 4.3},
        {"name": "Liberty Central",       "stars": 4, "price_per_night":
1_400_000, "area": "Quận 1",      "rating": 4.1},
        {"name": "Cochin Zen Hotel",      "stars": 3, "price_per_night":
550_000,   "area": "Quận 3",      "rating": 4.4},
        {"name": "The Common Room",       "stars": 2, "price_per_night":
180_000,   "area": "Quận 1",      "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa 2 thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đích (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy chuyến bay, trả về thông báo không có chuyến bay.
    """  
    flights = FLIGHTS_DB.get((origin, destination))
    current_origin, current_destination = origin, destination
    
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        if flights:
            current_origin, current_destination = destination, origin
            
    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}"
    
    def format_price(p):
        return f"{p:,}".replace(",", ".") + "đ"
        
    output = [f"Danh sách chuyến bay từ {current_origin} đến {current_destination}:"]
    for f in flights:
        price = format_price(f["price"])
        output.append(f"- {f['airline']}: {f['departure']} -> {f['arrival']}, Giá: {price}, Hạng: {f['class']}")
        
    return "\n".join(output)

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VD: 1000000), mặc định không giới hạn
    Trả về danh sách khách sạn với tên, số sao, giá, khu vực, đánh giá.
    Nếu không tìm thấy khách sạn, trả về thông báo không có khách sạn.
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy khách sạn tại {city}"

    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)
    
    def format_price(p):
        return f"{p:,}".replace(",", ".") + "đ"
        
    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
    
    output = [f"Danh sách khách sạn tại {city} (Sắp xếp theo đánh giá):"]
    for h in filtered_hotels:
        price = format_price(h["price_per_night"])
        output.append(f"- {h['name']} ({h['stars']}*): {price}/đêm, Khu vực {h['area']}, Đánh giá {h['rating']}/5")
        
    return "\n".join(output)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
    định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')

    Trả về: bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    def format_price(p):
        return f"{p:,}".replace(",", ".") + "đ"

    try:
        expense_dict = {}
        total_spent = 0
        # Tách các khoản chi bằng cả dấu phẩy và dấu xuống dòng
        import re
        lines = [l.strip() for l in re.split(',|\n', expenses) if l.strip()]
        
        for line in lines:
            if ':' not in line:
                raise ValueError(f"Định dạng chi phí sai: '{line}'. Vui lòng dùng 'Tên: Số tiền'")
            parts = line.split(':', 1)
            name = parts[0].strip()
            amount_str = parts[1].replace('.', '').replace(',', '').replace('đ', '').strip()
            
            if not amount_str.isdigit():
                raise ValueError(f"Số tiền không hợp lệ cho '{name}': {parts[1]}")
            
            amount = int(amount_str)
            expense_dict[name] = amount
            total_spent += amount
            
        remaining = total_budget - total_spent
        
        output = ["Bảng chi phí:"]
        for name, amount in expense_dict.items():
            output.append(f"- {name}: {format_price(amount)}")
            
        output.append("")
        output.append(f"Tổng chi: {format_price(total_spent)}")
        output.append(f"Ngân sách: {format_price(total_budget)}")
        output.append(f"Còn lại: {format_price(remaining)}")
        
        if remaining < 0:
            output.append(f"\nVượt ngân sách {format_price(abs(remaining))}! Cần điều chỉnh.")
            
        return "\n".join(output)
        
    except Exception as e:
        return f"Lỗi xử lý ngân sách: {str(e)}. Hãy đảm bảo cung cấp chi phí theo định dạng 'Tên: Số tiền' mỗi dòng."



