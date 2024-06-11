# Dockerize a Python web app

## 1. Create the app locally 

```console
$ python3 -m venv venv
$ . venv/bin/activate
$  pip install pandas
$  pip install openpyxl
```# TutorReporting
# TutorReporting




Simple
Input : File with Report
Output : StudentName_TestName_TestDate.csv (For Each Student)


project/
│
├── data/
│   ├── all_students_performance_report.csv  # Input report
│   └── reports/                             # Folder to store individual student reports
│       ├── Student1/
│       │   └── Student1_performance_report.csv
│       ├── Student2/
│       │   └── Student2_performance_report.csv
│       └── Student3/
│           └── Student2_performance_report.csv
│
├── script/
│   └── generate_individual_reports.py       # Python script to generate individual reports
│
└── README.md                                # Project documentation
