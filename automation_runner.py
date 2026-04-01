# import os
# import shutil
# import logging
# from datetime import datetime

# from config import INCOMING_DIR, OUTPUT_DIR, PROCESSED_DIR, ERROR_DIR, LOG_FILE
# from parser import parse_txt_file, build_portfolio_data
# from pdf_builder import build_portfolio_pdf


# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s"
# )


# def find_txt_files():
#     files = []
#     for file_name in os.listdir(INCOMING_DIR):
#         if file_name.lower().endswith(".txt"):
#             files.append(os.path.join(INCOMING_DIR, file_name))
#     return files


# def identify_files(txt_paths):
#     teh_file = None
#     rid_file = None

#     for path in txt_paths:
#         try:
#             with open(path, "rb") as f:
#                 file_bytes = f.read()

#             parsed = parse_txt_file(file_bytes)
#             property_name = parsed["property_name"]

#             if property_name == "TPS Tehachapi":
#                 teh_file = path
#             elif property_name == "TPS Ridgecrest":
#                 rid_file = path

#         except Exception as e:
#             logging.error(f"Failed to inspect file {path}: {e}")
#             shutil.move(path, os.path.join(ERROR_DIR, os.path.basename(path)))

#     return teh_file, rid_file


# def move_to_processed(file_path):
#     dest = os.path.join(PROCESSED_DIR, os.path.basename(file_path))
#     if os.path.exists(dest):
#         base, ext = os.path.splitext(os.path.basename(file_path))
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         dest = os.path.join(PROCESSED_DIR, f"{base}_{timestamp}{ext}")
#     shutil.move(file_path, dest)


# def main():
#     try:
#         txt_files = find_txt_files()

#         if not txt_files:
#             logging.info("No TXT files found in incoming folder.")
#             print("No TXT files found.")
#             return

#         teh_file, rid_file = identify_files(txt_files)

#         if not teh_file or not rid_file:
#             logging.info("Both required files are not available yet.")
#             print("Waiting for both Tehachapi and Ridgecrest files.")
#             return

#         with open(teh_file, "rb") as f1, open(rid_file, "rb") as f2:
#             portfolio_data = build_portfolio_data(f1.read(), f2.read())

#         today_str = datetime.today().strftime("%Y-%m-%d")
#         pdf_name = f"TownePlace_Suites_Portfolio_{today_str}.pdf"
#         output_path = os.path.join(OUTPUT_DIR, pdf_name)

#         build_portfolio_pdf(portfolio_data, output_path)

#         move_to_processed(teh_file)
#         move_to_processed(rid_file)

#         logging.info(f"PDF created successfully: {output_path}")
#         print(f"PDF created: {output_path}")

#     except Exception as e:
#         logging.exception(f"Automation failed: {e}")
#         print(f"Automation failed: {e}")


# if __name__ == "__main__":
#     main()


import os
import shutil
import logging
from datetime import datetime

from config import INCOMING_DIR, OUTPUT_DIR, PROCESSED_DIR, LOG_DIR
from parser import parse_txt_file, build_portfolio_data
from pdf_builder import build_portfolio_pdf

LOG_FILE = os.path.join(LOG_DIR, "automation.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def find_txt_files():
    files = []
    for file_name in os.listdir(INCOMING_DIR):
        if file_name.lower().endswith(".txt"):
            files.append(os.path.join(INCOMING_DIR, file_name))
    return files


def identify_files(txt_paths):
    teh_file = None
    rid_file = None

    for path in txt_paths:
        try:
            with open(path, "rb") as f:
                file_bytes = f.read()

            parsed = parse_txt_file(file_bytes)
            property_name = parsed["property_name"]

            if property_name == "TPS Tehachapi" and teh_file is None:
                teh_file = path
            elif property_name == "TPS Ridgecrest" and rid_file is None:
                rid_file = path

        except Exception as e:
            logging.error(f"Failed to inspect file {path}: {e}")

    return teh_file, rid_file


def move_to_processed(file_path):
    dest = os.path.join(PROCESSED_DIR, os.path.basename(file_path))
    if os.path.exists(dest):
        base, ext = os.path.splitext(os.path.basename(file_path))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(PROCESSED_DIR, f"{base}_{timestamp}{ext}")
    shutil.move(file_path, dest)


def run_automation():
    txt_files = find_txt_files()

    if not txt_files:
        return {
            "status": "waiting",
            "message": "No TXT files found in incoming folder."
        }

    teh_file, rid_file = identify_files(txt_files)

    if not teh_file or not rid_file:
        return {
            "status": "waiting",
            "message": "Both required files are not available yet."
        }

    with open(teh_file, "rb") as f1, open(rid_file, "rb") as f2:
        portfolio_data = build_portfolio_data(f1.read(), f2.read())

    today_str = datetime.today().strftime("%Y-%m-%d")
    pdf_name = f"TownePlace_Suites_Portfolio_{today_str}.pdf"
    output_path = os.path.join(OUTPUT_DIR, pdf_name)

    build_portfolio_pdf(portfolio_data, output_path)

    move_to_processed(teh_file)
    move_to_processed(rid_file)

    logging.info(f"PDF created successfully: {output_path}")

    return {
        "status": "success",
        "message": "PDF created successfully.",
        "pdf_name": pdf_name,
        "pdf_path": output_path
    }


def main():
    try:
        result = run_automation()
        print(result)
    except Exception as e:
        logging.exception(f"Automation failed: {e}")
        print({"status": "error", "message": str(e)})


if __name__ == "__main__":
    main()