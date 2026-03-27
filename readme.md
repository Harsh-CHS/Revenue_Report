D:\Revenue_Report_Automation\
│
├── app\
│   ├── app.py
│   ├── parser.py
│   ├── pdf_builder.py
│   ├── automation_runner.py
│   ├── config.py
│   └── requirements.txt
│
├── data\
│   ├── incoming\
│   ├── matched\
│   ├── processed\
│   ├── error\
│   └── output\
│
├── logs\
│   └── automation.log
│
└── archive\
    ├── txt\
    └── pdf\


What automation_runner.py will do:

check incoming/
find one Tehachapi txt and one Ridgecrest txt
parse them
create PDF
save PDF in output/
move txt files to processed/

Run:
For n8n: python automation_runner.py
For Manually: python -m streamlit run app.py