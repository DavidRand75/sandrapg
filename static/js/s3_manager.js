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
                console.log('Buckets:', response.buckets);
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
        const _this = this;  // Store reference to 'this' so it's available inside event handler

        // Listen for changes in the radio buttons
        $('.bucket-radio').change(function() {
            // Update the selectedBucket property with the selected bucket's value
            _this.selectedBucket = $(this).val();
            console.log('Selected bucket:', _this.selectedBucket);
        });
    }

    // Method to get the currently selected bucket
    getSelectedBucket() {
        return this.selectedBucket;
    }

    // Method to create a new bucket
    createBucket(bucketName) {
        console.log(`Creating a new bucket: ${bucketName}`);
        // Logic to create a new bucket using AWS SDK or API call
        // Example: s3.createBucket({Bucket: bucketName})
    }

    // Method to delete a bucket
    deleteBucket(bucketName) {
        console.log(`Deleting bucket: ${bucketName}`);
        // Logic to delete a bucket using AWS SDK or API call
        // Example: s3.deleteBucket({Bucket: bucketName})
    }

    // Method to list files (objects) in a specific bucket
    listFiles(bucketName) {
        console.log(`Listing files in bucket: ${bucketName}`);
        // Logic to list files in the bucket using AWS SDK or API call
        // Example: s3.listObjectsV2({Bucket: bucketName})
        // Return or handle the list of files here
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


