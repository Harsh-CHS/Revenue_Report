from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

PAGE_WIDTH, PAGE_HEIGHT = letter

# Page layout
LEFT = 55
RIGHT = PAGE_WIDTH - 55
CONTENT_WIDTH = RIGHT - LEFT

# Colors
HEADER_BG = colors.HexColor("#0B2E4F")
SECTION_BG = colors.HexColor("#D9E5F1")
ROW_ALT = colors.HexColor("#E9E9E9")
TEXT_DARK = colors.HexColor("#0B2E4F")
TEXT_BLACK = colors.black


def fmt_currency(v):
    return f"${v:,.2f}"


def fmt_percent(v):
    return f"{v:.2f}%"


def fmt_number(v):
    if float(v).is_integer():
        return f"{int(v)}"
    return f"{v:,.2f}"


def calc_variance(cur, prev, metric_type):
    if metric_type == "number":
        diff = cur - prev
        return f"{int(diff)}" if float(diff).is_integer() else f"{diff:,.2f}"

    if metric_type == "points":
        diff = cur - prev
        return f"{diff:.2f} pts"

    if metric_type == "percent":
        if prev == 0:
            return "-"
        pct = ((cur - prev) / prev) * 100
        return f"{pct:.1f}%"

    return "-"

def draw_header(c, report_date):
    header_height = 60
    y_top = PAGE_HEIGHT

    # Background
    c.setFillColor(HEADER_BG)
    c.rect(0, y_top - header_height, PAGE_WIDTH, header_height, fill=1, stroke=0)

    c.setFillColor(colors.white)

    # Center position
    center_y = y_top - (header_height / 2)

    # Line 1 (Title)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        PAGE_WIDTH / 2,
        center_y + 6,
        "H2H KPIs- Hotel Daily Report"
    )

    # Line 2 (Subtitle / Date)
    c.setFont("Helvetica", 10.5)
    c.drawCentredString(
        PAGE_WIDTH / 2,
        center_y - 10,
        f"{report_date}"
    )


def draw_section_title(c, y_top, title):
    bar_h = 24
    c.setFillColor(SECTION_BG)
    c.roundRect(LEFT - 2, y_top - bar_h, CONTENT_WIDTH + 4, bar_h, 7, fill=1, stroke=0)

    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(LEFT + 8, y_top - 16, title)

    return y_top - bar_h - 10


def draw_table(c, y_top, headers, rows, col_centers, metric_x, variance_right=None):
    """
    metric_x: left aligned metric label x
    col_centers: list of x centers for centered columns after metric
    variance_right: right-aligned x for final variance column (optional)
    """

    header_font = 10
    body_font = 10
    row_h = 26
    stripe_h = 20
    header_gap = 22

    # ---- column headers ----
    c.setFillColor(TEXT_DARK)
    c.setFont("Helvetica-Bold", header_font)

    header_y = y_top - 4

    c.drawString(metric_x, header_y, headers[0])

    for i, header in enumerate(headers[1:], start=1):
        if variance_right is not None and i == len(headers) - 1:
            c.drawRightString(variance_right, header_y, header)
        else:
            c.drawCentredString(col_centers[i - 1], header_y, header)

    # more space below column header row
    y = y_top - header_gap

    # ---- data rows ----
    for idx, row in enumerate(rows):
        if idx % 2 == 0:
            c.setFillColor(ROW_ALT)
            c.rect(LEFT + 6, y - (stripe_h / 2), CONTENT_WIDTH - 12, stripe_h, fill=1, stroke=0)

        c.setFillColor(TEXT_BLACK)
        c.setFont("Helvetica", body_font)

        text_y = y - 3

        c.drawString(metric_x, text_y, str(row[0]))

        for j, val in enumerate(row[1:], start=1):
            if variance_right is not None and j == len(row) - 1:
                c.drawRightString(variance_right, text_y, str(val))
            else:
                c.drawCentredString(col_centers[j - 1], text_y, str(val))

        y -= row_h

    return y


def build_portfolio_pdf(data, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)

    teh = data["tehachapi"]
    rid = data["ridgecrest"]
    report_date = data["report_date"]
    report_month = report_date.split(" ")[0]
    report_year = report_date.split(",")[1].strip()
    day_of_period = data["day_of_period"] or "?"

    draw_header(c, report_date)

    # Shared column geometry for 3-col sections
    metric_x = LEFT + 10
    center_1 = LEFT + 290
    center_2 = LEFT + 450

    # Section 1
    y = PAGE_HEIGHT - 88
    y = draw_section_title(c, y, "Daily Performance Snapshot")

    daily_headers = ["Metric", "TPS Tehachapi", "TPS Ridgecrest"]
    daily_rows = [
        (
            "Rooms Sold",
            f"{int(teh['daily']['rooms_sold'])} of {int(teh['daily']['available_rooms'])}",
            f"{int(rid['daily']['rooms_sold'])} of {int(rid['daily']['available_rooms'])}",
        ),
        ("Occupancy", fmt_percent(teh["daily"]["occupancy"]), fmt_percent(rid["daily"]["occupancy"])),
        ("ADR", fmt_currency(teh["daily"]["adr"]), fmt_currency(rid["daily"]["adr"])),
        ("RevPAR", fmt_currency(teh["daily"]["revpar"]), fmt_currency(rid["daily"]["revpar"])),
        ("Gross Revenue", fmt_currency(teh["daily"]["gross_revenue"]), fmt_currency(rid["daily"]["gross_revenue"])),
    ]

    y = draw_table(
        c,
        y,
        daily_headers,
        daily_rows,
        col_centers=[center_1, center_2],
        metric_x=metric_x
    )

    # Section 2
    y -= 4
    y = draw_section_title(c, y, f"{report_month} {report_year} Period-to-Date Performance")

    ptd_headers = ["Metric", "TPS Tehachapi", "TPS Ridgecrest"]
    ptd_rows = [
        ("Rooms Sold", fmt_number(teh["ptd"]["rooms_sold"]), fmt_number(rid["ptd"]["rooms_sold"])),
        ("Occupancy", fmt_percent(teh["ptd"]["occupancy"]), fmt_percent(rid["ptd"]["occupancy"])),
        ("ADR", fmt_currency(teh["ptd"]["adr"]), fmt_currency(rid["ptd"]["adr"])),
        ("RevPAR", fmt_currency(teh["ptd"]["revpar"]), fmt_currency(rid["ptd"]["revpar"])),
        ("Gross Revenue", fmt_currency(teh["ptd"]["gross_revenue"]), fmt_currency(rid["ptd"]["gross_revenue"])),
    ]

    y = draw_table(
        c,
        y,
        ptd_headers,
        ptd_rows,
        col_centers=[center_1, center_2],
        metric_x=metric_x
    )

    # Section 3
    y -= 4
    y = draw_section_title(
        c,
        y,
        f"{report_month} {report_year} Period-to-Date (Day {day_of_period}) vs Last Year – TPS Tehachapi"
    )

    metric_x_3 = LEFT + 10
    center_yr1 = LEFT + 220
    center_yr2 = LEFT + 355
    variance_right = RIGHT - 12

    comp_headers = ["Metric", report_year, str(int(report_year) - 1), "Variance"]
    comp_rows = [
        (
            "Rooms Sold",
            fmt_number(teh["ptd"]["rooms_sold"]),
            fmt_number(teh["last_year_ptd"]["rooms_sold"]),
            calc_variance(teh["ptd"]["rooms_sold"], teh["last_year_ptd"]["rooms_sold"], "number"),
        ),
        (
            "Occupancy",
            fmt_percent(teh["ptd"]["occupancy"]),
            fmt_percent(teh["last_year_ptd"]["occupancy"]),
            calc_variance(teh["ptd"]["occupancy"], teh["last_year_ptd"]["occupancy"], "points"),
        ),
        (
            "ADR",
            fmt_currency(teh["ptd"]["adr"]),
            fmt_currency(teh["last_year_ptd"]["adr"]),
            calc_variance(teh["ptd"]["adr"], teh["last_year_ptd"]["adr"], "percent"),
        ),
        (
            "RevPAR",
            fmt_currency(teh["ptd"]["revpar"]),
            fmt_currency(teh["last_year_ptd"]["revpar"]),
            calc_variance(teh["ptd"]["revpar"], teh["last_year_ptd"]["revpar"], "percent"),
        ),
        (
            "Gross Revenue",
            fmt_currency(teh["ptd"]["gross_revenue"]),
            fmt_currency(teh["last_year_ptd"]["gross_revenue"]),
            calc_variance(teh["ptd"]["gross_revenue"], teh["last_year_ptd"]["gross_revenue"], "percent"),
        ),
    ]

    y = draw_table(
        c,
        y,
        comp_headers,
        comp_rows,
        col_centers=[center_yr1, center_yr2],
        metric_x=metric_x_3,
        variance_right=variance_right
    )

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawString(
        LEFT,
        18,
        "Generated automatically from uploaded Tehachapi and Ridgecrest TXT revenue reports."
    )

    c.save()