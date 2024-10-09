
$(document).ready(function() {

    // Usage Example:
    const s3Manager = new S3Manager();

    // Example usage: Call getSelectedFiles() to retrieve the checked files
    $('#download-files-btn').click(function() {
        const selectedFiles = s3Manager.getSelectedFiles();
        console.log('Selected files:', selectedFiles);
    });

    // Set up event listener for the delete button
    $('#delete-bucket-btn').click(() => {
        // Assume that s3Manager is the instance of your S3Manager class
        const bucketToDelete = s3Manager.getSelectedBucket();  // Get the selected bucket using getSelectedBucket()

        console.log("deleting: bucketToDelete", )
        // Check if a bucket is selected
        if (bucketToDelete) {
            // Confirm the deletion action
            const confirmed = confirm(`Are you sure you want to delete the bucket: ${bucketToDelete}?`);

            // If the user confirms, call the deleteBucket function in the S3Manager class
            if (confirmed) {
                s3Manager.deleteBucket(bucketToDelete);  // Call deleteBucket only if user confirms
            }
        } else {
            // Alert the user if no bucket is selected
            console.log("No bucket selected for deletion.");
        }
    });

    // Set up event listener for the create button
    $('#create-bucket-btn').click(() => {
        // Prompt the user to enter the new bucket name
        const newBucketName = prompt("Please enter the name of the new bucket:");

        // Check if the user entered a valid bucket name
        if (newBucketName) {
            // Call the createBucket method in S3Manager to create the new bucket
            s3Manager.createBucket(newBucketName);
        } else {
            // Alert the user if no name was entered
            alert("Bucket name is required to create a new bucket.");
        }
    });

    // Set up the event listener for the delete files button
    $('#delete-files-btn').click(() => {
        s3Manager.deleteSelectedFiles();  // Call the deleteSelectedFiles() method
    });

    // Listing buckets
    s3Manager.listBuckets();

    // Listing files in a bucket
    s3Manager.listFiles('existing-bucket-name');

    // Uploading a file to a bucket
    const fileToUpload = { name: 'example.txt' }; // Replace with actual file object
    s3Manager.uploadFile('existing-bucket-name', fileToUpload);

    // Downloading a file from a bucket
    s3Manager.downloadFile('existing-bucket-name', 'example.txt');

    // Deleting a file from a bucket
    s3Manager.deleteFile('existing-bucket-name', 'example.txt');

    // Deleting a bucket
    s3Manager.deleteBucket('new-bucket-name');

});