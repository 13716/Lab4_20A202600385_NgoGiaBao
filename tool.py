from __future__ import annotations

from langchain_core.tools import tool

# =========================
# MOCK DATABASE
# =========================

FLIGHTS_DB = {
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"},
    ],
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:30", "arrival": "07:50", "price": 1400000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "09:00", "arrival": "10:20", "price": 900000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "15:00", "arrival": "16:20", "price": 1200000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 800000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "17:00", "arrival": "18:20", "price": 1100000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 200000, "area": "Quận 1", "rating": 4.6},
    ],
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Melia", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
    ],
}

# =========================
# NORMALIZE INPUT
# =========================

CITY_MAP = {
    # Hà Nội
    "ha noi": "Hà Nội",
    "hà nội": "Hà Nội",
    "hanoi": "Hà Nội",
    "hn": "Hà Nội",
    "ha noi city": "Hà Nội",

    # Hồ Chí Minh
    "hcm": "Hồ Chí Minh",
    "tp hcm": "Hồ Chí Minh",
    "tphcm": "Hồ Chí Minh",
    "ho chi minh": "Hồ Chí Minh",
    "ho chi minh city": "Hồ Chí Minh",
    "hồ chí minh": "Hồ Chí Minh",
    "sai gon": "Hồ Chí Minh",
    "sài gòn": "Hồ Chí Minh",
    "sg": "Hồ Chí Minh",

    # Đà Nẵng
    "da nang": "Đà Nẵng",
    "đà nẵng": "Đà Nẵng",
    "danang": "Đà Nẵng",
    "dn": "Đà Nẵng",

    # Phú Quốc
    "phu quoc": "Phú Quốc",
    "phú quốc": "Phú Quốc",
    "pq": "Phú Quốc",

    # Nha Trang (nếu sau này thêm DB)
    "nha trang": "Nha Trang",
    "nt": "Nha Trang",

    # Huế
    "hue": "Huế",
    "huế": "Huế",

    # Cần Thơ
    "can tho": "Cần Thơ",
    "cần thơ": "Cần Thơ",
}


def normalize_city(name: str) -> str:
    key = name.strip().lower()
    return CITY_MAP.get(key, name.strip())


def format_vnd(price: int) -> str:
    return f"{price:,}".replace(",", ".") + "đ"

# =========================
# TOOLS
# =========================

@tool
def search_flights(
    origin: str,
    destination: str,
    date: str = "",
    passengers: int = 1,
    max_price: int | None = None,
) -> str:
    """Tìm chuyến bay giữa 2 thành phố. Gọi tool ngay khi có điểm đi + điểm đến."""

    o = normalize_city(origin)
    d = normalize_city(destination)

    print(f"[TOOL] search_flights: {o} → {d} | date={date} | pax={passengers}")

    flights = FLIGHTS_DB.get((o, d))

    if not flights:
        return f"Không tìm thấy chuyến bay từ {o} đến {d}."

    # filter theo giá nếu có
    if max_price:
        flights = [f for f in flights if f["price"] <= max_price]

    # sort theo giá
    flights = sorted(flights, key=lambda x: x["price"])

    # lấy top 3
    flights = flights[:3]

    lines = []
    for i, f in enumerate(flights, 1):
        lines.append(
            f"{i}. {f['airline']} | {f['departure']}–{f['arrival']} | {format_vnd(f['price'])} | {f['class']}"
        )

    return "\n".join(lines)


@tool
def search_hotels(city: str, max_price_per_night: int = 9999999, limit: int = 3) -> str:
    """Tìm khách sạn theo thành phố."""

    c = normalize_city(city)

    print(f"[TOOL] search_hotels: {c} | max_price={max_price_per_night}")

    hotels = HOTELS_DB.get(c)
    if not hotels:
        return f"Không tìm thấy khách sạn tại {c}."

    filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    filtered = sorted(filtered, key=lambda x: x["rating"], reverse=True)[:limit]

    lines = []
    for i, h in enumerate(filtered, 1):
        lines.append(
            f"{i}. {h['name']} | {h['stars']}★ | {format_vnd(h['price_per_night'])}/đêm | {h['area']}"
        )

    return "\n".join(lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính tổng chi phí."""

    print(f"[TOOL] calculate_budget: budget={total_budget}, expenses={expenses}")

    total_cost = 0
    for item in expenses.split(","):
        if ":" not in item:
            continue
        _, value = item.split(":")
        total_cost += int(value.strip())

    remaining = total_budget - total_cost

    return (
        f"Tổng chi: {format_vnd(total_cost)}\n"
        f"Ngân sách: {format_vnd(total_budget)}\n"
        f"Còn lại: {format_vnd(remaining)}"
    )
