import pandas as pd

# Load the Excel file
file_path = './Skill-Assesment.xlsx'
df = pd.read_excel(file_path, sheet_name=None)

# Extract skill tags and answer key
data = df['Form Responses 1']
skill_tags = data.iloc[0, 4:-1].values
answer_key = data.iloc[1, 4:-1].values

# Drop the first two rows (metadata) and reset index
student_data = data.drop([0, 1]).reset_index(drop=True)

# Function to calculate performance for each skill tag
def calculate_performance(student_row, skill_tags, answer_key):
    performance = {skill: {'correct': 0, 'total': 0} for skill in skill_tags}
    
    for i, skill in enumerate(skill_tags):
        # Check the student's answer against the answer key
        if student_row.iloc[4 + i] == answer_key[i]:
            performance[skill]['correct'] += 1
        performance[skill]['total'] += 1
    
    return performance

# Prepare a list to store each student's report data
report_data = []

# Iterate through each student and calculate their performance
for idx, row in student_data.iterrows():
    email = row['Email Address']
    submission_date = row['Timestamp']  # Add submission date
    student_performance = calculate_performance(row, skill_tags, answer_key)
    
    # Prepare the student's report data
    student_report = {'Student': email, 'Submission_Date': submission_date}
    for skill in skill_tags:
        correct = student_performance[skill]['correct']
        total = student_performance[skill]['total']
        student_report[skill] = f"{correct}/{total}"
    
    report_data.append(student_report)

# Create a DataFrame from the report data
report_df = pd.DataFrame(report_data)

# Ensure all data is treated as text
report_df = report_df.astype(str)

# Save the DataFrame to an Excel file
report_file_path = './all_students_performance_report.xlsx'
report_df.to_excel(report_file_path, index=False)

report_file_path
