
$(document).ready(function() {

    // Usage Example:
    const s3Manager = new S3Manager();

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