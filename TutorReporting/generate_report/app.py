import json
import boto3
import pandas as pd
from io import BytesIO
import uuid
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['GENERATEREPORTBUCKET_BUCKET_NAME']

def lambda_handler(event, context):
    # Extract bucket name and file key from the S3 event
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Download the Excel file from S3
    excel_object = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = excel_object['Body'].read()
    
    # Load the Excel file into a DataFrame
    df = pd.read_excel(BytesIO(file_content), sheet_name=None)
    
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
    
    # Convert the DataFrame to an Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        report_df.to_excel(writer, index=False)
    output.seek(0)
    
    # Generate a UUID for the output file key
    unique_id = uuid.uuid4()
    output_file_key = f"performance_reports/{unique_id}_performance_report.xlsx"
    
    # Upload the result back to S3
    s3.put_object(Bucket=BUCKET_NAME, Key=output_file_key, Body=output.getvalue(), ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    # Generate a presigned URL for the uploaded file, valid for 30 minutes
    presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': output_file_key}, ExpiresIn=1800)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f"Report generated and uploaded to {output_file_key}", 'presigned_url': presigned_url})
    }
