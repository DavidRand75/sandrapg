class S3Manager {

    constructor() {
        
        this.bucketList = [];  // Store the list of buckets
        this.selectedBucket = null;  // Member variable to store the selected bucket

        this.init();
    }

    // Initialize the S3Manager by calling listBuckets via AJAX
    init() {
        console.log('Initializing S3 Manager...');
        this.listBuckets();
    }

    // Perform an AJAX call to list the buckets from the backend
    listBuckets() {
        $.ajax({
            url: '/list_buckets',
            type: 'GET',
            success: (response) => {
                this.bucketList = response.buckets; 
                //console.log('Buckets in prop:', this.bucketList);  // Log the filled bucket list
                // Clear the bucket list before appending new items
                $('#bucket-list').empty();

                // Append each bucket as a list item with a radio button
                response.buckets.forEach(bucket => {
                    $('#bucket-list').append(
                        `<li class="list-group-item" id="bucket-${bucket}">
                            <input type="radio" name="bucket" value="${bucket}" class="mr-2 bucket-radio"> 
                            ${bucket}
                         </li>`
                    );
                });

                // Set up the event listener to update the selected bucket
                this.setupRadioButtonListener();
            },
            error: function(error) {
                console.error('Error fetching bucket list:', error);
            }
        });
    }

    // Set up event listener to track which bucket is selected
    setupRadioButtonListener() {
        // Use an arrow function to maintain the context of 'this'
        $('.bucket-radio').change((event) => {
            // Update the selectedBucket property with the selected bucket's value
            this.selectedBucket = $(event.target).val();
            console.log('Selected bucket:', this.selectedBucket);  // Log the selected bucket

            // Now that we have the selected bucket, list its files
            this.listFiles();
        });
    }


    // Method to list files in the selected bucket
    listFiles() {
        const selectedBucket = this.selectedBucket;

        if (!selectedBucket) {
            console.log('First load - No bucket selected.');
            return;
        }

        //console.log(`Listing files in bucket: ${this.selectedBucket}`);

        $.ajax({
            url: '/list_files',
            type: 'GET',
            data: { bucket: selectedBucket },  // Send the selected bucket as a query parameter
            success: (response) => {
                // Clear the file list before appending new files
                $('#file-list').empty();

                if (response.files && response.files.length > 0) {
                    response.files.forEach(file => {
                        $('#file-list').append(`
                            <li class="list-group-item">
                                <input type="checkbox" class="file-checkbox" value="${file}">
                                ${file}
                            </li>
                        `);
                    });
                } else {
                    $('#file-list').append(`<li class="list-group-item">No files found in bucket</li>`);
                }
            },
            error: (error) => {
                console.error(`Error listing files in bucket ${selectedBucket}:`, error);
            }
        });
    }

    // Method to get the currently selected bucket
    getSelectedBucket() {
        return this.selectedBucket;
    }

    // Function to get the selected files (checked checkboxes)
    getSelectedFiles() {
        let selectedFiles = [];

        $('.file-checkbox:checked').each(function() {
            selectedFiles.push($(this).val());  // Add file name to array
        });

        return selectedFiles;
    }

    // Method to create a new bucket
    createBucket(bucketName) {
        console.log(`Creating a new bucket: ${bucketName}`);
        
        $.ajax({
            url: '/create_bucket',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ bucket_name: bucketName }),
            success: (response) => {
                console.log(`Bucket ${bucketName} created successfully.`);
                this.listBuckets();  // Refresh the bucket list after creation
            },
            error: (error) => {
                console.error(`Error creating bucket: ${bucketName}`, error);
            }
        });
    }

    // Method to delete a bucket
    deleteBucket(bucketName) {
        console.log(`Deleting bucket: ${bucketName}`);
        
        $.ajax({
            url: '/delete_bucket',
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({ bucket_name: bucketName }),
            success: (response) => {
                console.log(`Bucket ${bucketName} deleted successfully.`);
                this.listBuckets();  // Refresh the bucket list after deletion
            },
            error: (error) => {
                console.error(`Error deleting bucket: ${bucketName}`, error);
            }
        });
    }

    // Method to upload a file to a bucket
    uploadFile(bucketName, file) {
        console.log(`Uploading file: ${file.name} to bucket: ${bucketName}`);
        // Logic to upload a file to the bucket using AWS SDK or API call
        // Example: s3.putObject({Bucket: bucketName, Key: file.name, Body: file})
    }

    // Method to download a file from a bucket
    downloadFile(bucketName, fileName) {
        console.log(`Downloading file: ${fileName} from bucket: ${bucketName}`);
        // Logic to download a file from the bucket using AWS SDK or API call
        // Example: s3.getObject({Bucket: bucketName, Key: fileName})
    }

    // Method to delete a file from a bucket
    deleteFile(bucketName, fileName) {
        console.log(`Deleting file: ${fileName} from bucket: ${bucketName}`);
        // Logic to delete a file from the bucket using AWS SDK or API call
        // Example: s3.deleteObject({Bucket: bucketName, Key: fileName})
    }
}


