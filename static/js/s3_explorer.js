
$(document).ready(function() {

    // Usage Example:
    const s3Manager = new S3Manager();

    // Example usage: Call getSelectedFiles() to retrieve the checked files
    $('#download-files-btn').click(function() {
        const selectedFiles = s3Manager.getSelectedFiles();
        console.log('Selected files:', selectedFiles);
    });

    // Listing buckets
    s3Manager.listBuckets();

    // Creating a new bucket
    s3Manager.createBucket('new-bucket-name');

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