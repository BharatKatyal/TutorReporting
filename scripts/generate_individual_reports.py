
import pandas as pd
import os

# Define paths
input_excel_path = './Skill-Assesment.xlsx'
output_dir = './data/reports/'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the Excel file
df = pd.read_excel(input_excel_path, sheet_name=None)

# Extract skill tags and answer key
data = df['Form Responses 1']
skill_tags = data.iloc[0, 4:-1].values
answer_key = data.iloc[1, 4:-1].values

# Drop the first two rows (metadata) and reset index
student_data = data.drop([0, 1]).reset_index(drop=True)

# Function to calculate performance for each skill tag
def calculate_performance(student_row, skill_tags, answer_key):
    performance = {skill: {'correct': 0, 'total': 0} for skill in set(skill_tags)}
    
    for i, skill in enumerate(skill_tags):
        # Check the student's answer against the answer key
        if student_row.iloc[4 + i] == answer_key[i]:
            performance[skill]['correct'] += 1
        performance[skill]['total'] += 1
    
    return performance

# Process each student
for idx, row in student_data.iterrows():
    email = row['Email Address']
    timestamp = row['Timestamp']
    student_name = email.replace('@', '_at_')
    student_dir = os.path.join(output_dir, student_name)
    
    # Create directory for the student if it doesn't exist
    os.makedirs(student_dir, exist_ok=True)
    
    # Calculate student performance
    student_performance = calculate_performance(row, skill_tags, answer_key)
    
    # Prepare the student's report data
    student_report = {'Skill': [], 'Total (Correct/Total)': [], 'Total Percentage': [], 'Timestamp': timestamp}
    for skill in student_performance:
        correct = student_performance[skill]['correct']
        total = student_performance[skill]['total']
        percentage = (correct / total) * 100 if total > 0 else 0
        student_report['Skill'].append(skill)
        student_report['Total (Correct/Total)'].append(f"{correct}/{total}")
        student_report['Total Percentage'].append(f"{percentage:.2f}%")
    
    # Create a DataFrame for the student's report
    report_df = pd.DataFrame(student_report)
    
    # Generate the report file name
    report_file_name = f"{student_name}_performance_report_{timestamp}.csv"
    report_file_path = os.path.join(student_dir, report_file_name)
    
    # Save the individual report
    report_df.to_csv(report_file_path, index=False)

print("Individual student performance reports have been generated.")
