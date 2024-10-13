from flask import Flask, render_template, jsonify, request, url_for, session, redirect
from s3_manager import S3Manager
from alglist import alglist
import zmq
import json



import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Ensure the shared directory exists before starting download workers
SHARED_DOWNLOAD_DIR = os.getenv('SHARED_DOWNLOAD_DIR', '/tmp/shared_audio_files')
os.makedirs(SHARED_DOWNLOAD_DIR, exist_ok=True)  # This runs before any worker starts


# Retrieve environment variables
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')
flask_session_key = os.getenv('FLASK_SESSION_KEY')

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = flask_session_key

# Initialize ZeroMQ Context and PUB socket
context = zmq.Context()
socket = context.socket(zmq.PUSH)
# Set the queue size (high water mark) to 1000 messages
socket.setsockopt(zmq.SNDHWM, 1000)  # This sets the maximum number of queued messages to 1000

# Bind the PUB socket only once when the app starts
try:
    socket.bind("tcp://*:5557")  # Use port 5557 for PUB
    print("ZeroMQ PUB socket bound to port 5557")
except zmq.ZMQError as e:
    print(f"Failed to bind ZeroMQ PUB socket to port 5557: {e}")




# Define the route for the home pagepython 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list_buckets', methods=['GET'])
def list_buckets():
    global s3_manager

    buckets = s3_manager.list_buckets()
    if buckets:
        return jsonify({'buckets': buckets}), 200
    else:
        return jsonify({'error': 'Unable to list buckets'}), 500
    
@app.route('/list_files', methods=['GET'])
def list_files():
    global s3_manager

    bucket_name = request.args.get('bucket')  # Get the bucket name from the query parameters
    if not bucket_name:
        return jsonify({'error': 'Bucket name is required'}), 400

    try:
        # Call the s3_manager to list files in the bucket
        files = s3_manager.list_files(bucket_name)
        
        # If files exist, return them; otherwise, return an empty list
        if files is not None:
            if len(files) > 0:
                return jsonify({'files': files}), 200  # Return the list of files
            else:
                return jsonify({'files': []}), 200  # Return an empty list if no files found
        else:
            return jsonify({'error': f'Unable to retrieve files from bucket: {bucket_name}'}), 500

    except Exception as e:
        # Catch any unexpected errors and return a 500 response
        print(f"Error listing files in bucket {bucket_name}: {e}")
        return jsonify({'error': 'An error occurred while retrieving files'}), 500
    
@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    global s3_manager

    data = request.get_json()
    bucket_name = data.get('bucket_name')

    if not bucket_name:
        return jsonify({'error': 'Bucket name is required'}), 400

    success = s3_manager.create_bucket(bucket_name)
    if success:
        return jsonify({'message': f'Bucket {bucket_name} created successfully'}), 200
    else:
        return jsonify({'error': f'Failed to create bucket {bucket_name}'}), 500

@app.route('/delete_bucket', methods=['DELETE'])
def delete_bucket():
    global s3_manager

    data = request.get_json()
    bucket_name = data.get('bucket_name')

    if not bucket_name:
        return jsonify({'error': 'Bucket name is required'}), 400

    success = s3_manager.delete_bucket(bucket_name)
    if success:
        return jsonify({'message': f'Bucket {bucket_name} deleted successfully'}), 200
    else:
        return jsonify({'error': f'Failed to delete bucket {bucket_name}'}), 500

@app.route('/delete_files', methods=['DELETE'])
def delete_files():
    global s3_manager

    data = request.get_json()
    bucket_name = data.get('bucket_name')
    files_to_delete = data.get('files', [])

    if not bucket_name:
        return jsonify({'error': 'Bucket name is required'}), 400

    if len(files_to_delete) == 0:
        return jsonify({'error': 'No files specified for deletion'}), 400

    success = s3_manager.delete_files(bucket_name, files_to_delete)
    if success:
        return jsonify({'message': 'Files deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete files'}), 500
    
@app.route('/upload_files', methods=['POST'])
def upload_files():
    global s3_manager

    bucket_name = request.form['bucket_name']
    files = request.files.getlist('files')

    if not bucket_name:
        return jsonify({'error': 'Bucket name is required'}), 400

    if len(files) == 0:
        return jsonify({'error': 'No files selected for upload'}), 400

    success = s3_manager.upload_files(bucket_name, files)
    if success:
        return jsonify({'message': 'Files uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Failed to upload files'}), 500
    
@app.route('/generate_presigned_url', methods=['POST'])
def generate_presigned_url():
    global s3_manager
    data = request.get_json()
    bucket_name = data.get('bucket_name')
    files = data.get('files', [])

    if not bucket_name or not files:
        return jsonify({'error': 'Bucket name and files are required'}), 400

    presigned_urls = []

    for file_name in files:
        url = s3_manager.generate_presigned_url(bucket_name, file_name)
        if url:
            presigned_urls.append({'file_name': file_name, 'url': url})

    return jsonify({'presigned_urls': presigned_urls}), 200

@app.route('/process_files', methods=['POST'])
def process_files():
    try:
        data = request.get_json()
        if not data:
            print("No data received from request")
            return {'error': 'No data received'}, 400
        
        accumulated_files = data.get('accumulatedFiles')
        if not accumulated_files:
            print("No accumulatedFiles found in the data")
            return {'error': 'No accumulatedFiles provided'}, 400

        print("Accumulated files received:", accumulated_files)

        # Store accumulated_files in the session
        session['accumulated_files'] = accumulated_files

        # Redirect to the new template
        return {'redirect_url': url_for('show_accumulated_files')}
    
    except Exception as e:
        print(f"Error processing files: {e}")
        return {'error': str(e)}, 500

@app.route('/show_accumulated_files')
def show_accumulated_files():
    accumulated_files = session.get('accumulated_files', {})
    return render_template('show_accumulated_files.html', accumulated_files=accumulated_files,alglist=alglist)
'''
@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()  # Get the dictionary from the frontend
    selected_files = data.get('files', {})
    selected_algorithms = data.get('algorithms', [])

    # Here you can process the files and algorithms as needed
    print("Selected Files:", selected_files)
    print("Selected Algorithms:", selected_algorithms)

    tasks = []

    # Iterate over each bucket and its files
    for bucket, files in selected_files.items():
        for file in files:
            # Create a task for each file and each algorithm
            for algorithm in selected_algorithms:
                task = (bucket, file, algorithm)
                tasks.append(task)

                # Log the task and its type for debugging
                task_json = json.dumps(task)
                print(f"Sending task: {task_json}, Type: {type(task_json)}")
                try:
                    # Send the task in non-blocking mode
                    socket.send_string(task_json, zmq.NOBLOCK)
                except zmq.Again:
                    # If the queue is full, log the event
                    print(f"Queue full, could not send task: {task_json}")

    print("Generated Tasks:", tasks)  

    # Send a response back to the frontend
    return jsonify({'message': 'Processing initiated', 'status': 'success'})
'''

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()  # Get the dictionary from the frontend
    selected_files = data.get('files', {})
    selected_algorithms = data.get('algorithms', [])

    # Here you can process the files and algorithms as needed
    print("Selected Files:", selected_files)
    print("Selected Algorithms:", selected_algorithms)

    tasks = []

   # Iterate over each bucket and its files
    for bucket, files in selected_files.items():
        for file in files:
            # Create a task for each file with all selected algorithms
            task = {
                'bucket': bucket,
                'file': file,
                'algorithms': selected_algorithms  # Pass the entire list of algorithms
            }

            # Log the task and its type for debugging
            task_json = json.dumps(task)
            print(f"Sending task: {task_json}, Type: {type(task_json)}")

            try:
                # Send the task in non-blocking mode
                socket.send_string(task_json, zmq.NOBLOCK)
            except zmq.Again:
                # If the queue is full, log the event
                print(f"Queue full, could not send task: {task_json}")

            # Add task to list for tracking (if needed)
            tasks.append(task)

    print("Generated Tasks:", tasks)

    # Send a response back to the frontend
    return jsonify({'message': 'Processing initiated', 'status': 'success'})
if __name__ == '__main__':

    # Pass environment variables to S3Manager
    s3_manager = S3Manager(aws_access_key, aws_secret_key, aws_region)

    #app.run(debug=True)
    app.run(debug=False, threaded=False)
    