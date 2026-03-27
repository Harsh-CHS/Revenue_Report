import re
from datetime import datetime


def clean_number(value: str) -> float:
    value = value.replace(",", "").strip()

    if value in {".00", ".", ""}:
        return 0.0

    if value.endswith("-"):
        value = "-" + value[:-1]

    return float(value)


def format_report_date(date_str: str) -> str:
    # 15Mar26 -> March 15, 2026
    dt = datetime.strptime(date_str, "%d%b%y")
    return dt.strftime("%B %d, %Y")


def extract_source_report_date(text: str) -> str:
    match = re.search(r"(\d{2}[A-Za-z]{3}\d{2})\s+Run on", text)
    if not match:
        return "Unknown Date"
    return format_report_date(match.group(1))


def extract_day_of_period(text: str) -> str:
    match = re.search(r"\(DAY\s+(\d+)\s+OF PERIOD\s+(\d+)\)", text, flags=re.IGNORECASE)
    if not match:
        return ""
    return match.group(1)


def detect_property(text: str) -> str:
    if "TownePlace Suites Tehachapi" in text:
        return "TPS Tehachapi"
    if "TownePlace Suites Ridgecrest" in text:
        return "TPS Ridgecrest"
    return "Unknown Property"


def extract_metric_line(text: str, label: str):
    pattern = rf"^\s*{re.escape(label)}\s+([.\d,\-]+)\s+([.\d,\-]+)\s+([.\d,\-]+)\s+([.\d,\-]+)\s+([.\d,\-]+)\s+([.\d,\-]+)\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE)

    if not match:
        return None

    vals = [clean_number(v) for v in match.groups()]
    return vals


def parse_tehachapi(text: str):
    rooms_sold = extract_metric_line(text, "# ROOMS SOLD")
    available = extract_metric_line(text, "# AVAILABLE FOR SALE")
    occupancy = extract_metric_line(text, "OCCUPANCY PCT")
    adr = extract_metric_line(text, "AVG RATE PER ROOM")
    revpar = extract_metric_line(text, "REV PAR")
    gross = extract_metric_line(text, "GROSS HOTEL SALES")

    return {
        "property_name": "TPS Tehachapi",
        "daily": {
            "rooms_sold": rooms_sold[0],
            "available_rooms": available[0],
            "occupancy": occupancy[0],
            "adr": adr[0],
            "revpar": revpar[0],
            "gross_revenue": gross[0],
        },
        "ptd": {
            "rooms_sold": rooms_sold[2],
            "occupancy": occupancy[2],
            "adr": adr[2],
            "revpar": revpar[2],
            "gross_revenue": gross[2],
        },
        "last_year_ptd": {
            "rooms_sold": rooms_sold[3],
            "occupancy": occupancy[3],
            "adr": adr[3],
            "revpar": revpar[3],
            "gross_revenue": gross[3],
        },
    }


def parse_ridgecrest(text: str):
    rooms_sold = extract_metric_line(text, "# ROOMS SOLD")
    available = extract_metric_line(text, "# AVAILABLE FOR SALE")
    occupancy = extract_metric_line(text, "OCCUPANCY PCT")
    adr = extract_metric_line(text, "AVG RATE PER ROOM")
    revpar = extract_metric_line(text, "REV PAR")
    gross = extract_metric_line(text, "GROSS HOTEL SALES")

    return {
        "property_name": "TPS Ridgecrest",
        "daily": {
            "rooms_sold": rooms_sold[0],
            "available_rooms": available[0],
            "occupancy": occupancy[0],
            "adr": adr[0],
            "revpar": revpar[0],
            "gross_revenue": gross[0],
        },
        "ptd": {
            "rooms_sold": rooms_sold[2],
            "occupancy": occupancy[2],
            "adr": adr[2],
            "revpar": revpar[2],
            "gross_revenue": gross[2],
        },
    }


def parse_txt_file(file_bytes: bytes):
    text = file_bytes.decode("utf-8", errors="ignore")
    property_name = detect_property(text)
    report_date = extract_source_report_date(text)
    day_of_period = extract_day_of_period(text)

    if property_name == "TPS Tehachapi":
        data = parse_tehachapi(text)
    elif property_name == "TPS Ridgecrest":
        data = parse_ridgecrest(text)
    else:
        raise ValueError("Could not identify property from uploaded file.")

    data["report_date"] = report_date
    data["day_of_period"] = day_of_period
    return data


def build_portfolio_data(file1_bytes: bytes, file2_bytes: bytes):
    d1 = parse_txt_file(file1_bytes)
    d2 = parse_txt_file(file2_bytes)

    files = {
        d1["property_name"]: d1,
        d2["property_name"]: d2,
    }

    if "TPS Tehachapi" not in files or "TPS Ridgecrest" not in files:
        raise ValueError("Please upload exactly one Tehachapi file and one Ridgecrest file.")

    teh = files["TPS Tehachapi"]
    rid = files["TPS Ridgecrest"]

    return {
        "report_date": teh["report_date"],
        "day_of_period": teh["day_of_period"],
        "tehachapi": teh,
        "ridgecrest": rid,
    }