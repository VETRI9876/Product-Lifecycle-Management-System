from flask import Flask, request, jsonify
import mysql.connector
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

db_config = {
    'host': 'database-1.cne4ogysyg9x.eu-north-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'Vetri123231',
    'database': 'vetri_db'
}

S3_BUCKET = 'vetri-devops-bucket'
S3_REGION = 'eu-north-1'

s3 = boto3.client('s3', region_name=S3_REGION)

@app.route('/')
def home():
    return "Welcome to Vetri's Flask App connected to RDS and S3!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)

    s3.upload_fileobj(file, S3_BUCKET, filename)

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO uploads (filename) VALUES (%s)"
        cursor.execute(query, (filename,))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': f'{filename} uploaded successfully to S3 and recorded in RDS'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
