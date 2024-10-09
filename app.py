from flask import Flask, render_template, jsonify, request
from s3_manager import S3Manager

import os
from dotenv import load_dotenv


# Load the .env file
load_dotenv()


# Retrieve environment variables
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

# Pass environment variables to S3Manager
s3_manager = S3Manager(aws_access_key, aws_secret_key, aws_region)


app = Flask(__name__)

# Define the route for the home pagepython 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list_buckets', methods=['GET'])
def list_buckets():
    buckets = s3_manager.list_buckets()
    if buckets:
        return jsonify({'buckets': buckets}), 200
    else:
        return jsonify({'error': 'Unable to list buckets'}), 500
    
@app.route('/list_files', methods=['GET'])
def list_files():
    bucket_name = request.args.get('bucket')  # Get the bucket name from the query parameters
    if bucket_name:
        files = s3_manager.list_files(bucket_name)
        if files:
            return jsonify({'files': files}), 200
        else:
            return jsonify({'error': f'No files found in bucket: {bucket_name}'}), 404
    else:
        return jsonify({'error': 'Bucket name is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
