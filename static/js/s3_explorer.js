
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

    // Event listener to show the modal when the "Upload File" button is clicked
    $('#upload-file-btn').click(() => {
        $('#uploadFilesModal').modal('show');  // Show the modal
    });

    // Event listener for the upload button inside the modal
    $('#confirm-upload-btn').click(() => {
        const files = $('#file-input')[0].files;  // Get the selected files from the input

        if (files.length === 0) {
            alert("No files selected.");
            return;
        }

        s3Manager.uploadFiles(files);  // Call the uploadFiles method from S3Manager

        // Close the modal after the upload is triggered
        $('#uploadFilesModal').modal('hide');
    });

    // Event listener to update the file list when files are selected
    $('#file-input').change(function() {
        const fileList = $('#file-input')[0].files;  // Get the selected files
        const fileDisplayList = $('#selected-file-list');  // The UL element to display the files

        // Clear the file display list before populating it with new selections
        fileDisplayList.empty();

        // Iterate over the selected files and display them in the list
        for (let i = 0; i < fileList.length; i++) {
            const fileName = fileList[i].name;
            fileDisplayList.append(`<li class="list-group-item">${fileName}</li>`);
        }
    });

    // Event listener for the upload button inside the modal
    $('#confirm-upload-btn').click(() => {
        const files = $('#file-input')[0].files;  // Get the selected files from the input

        if (files.length === 0) {
            alert("No files selected.");
            return;
        }

        s3Manager.uploadFiles(files);  // Call the uploadFiles method from S3Manager

        // Close the modal after the upload is triggered
        $('#uploadFilesModal').modal('hide');

        // Clear the selected file list and the file input after upload
        $('#selected-file-list').empty();
        $('#file-input').val(null);  // Clear the input field to reset the file selection
    });

    // Clear file list when the modal is hidden (closed)
    $('#uploadFilesModal').on('hidden.bs.modal', function () {
        $('#selected-file-list').empty();  // Clear the file display list
        $('#file-input').val(null);  // Clear the input field
    });

    // Event listener for the download button
    $('#download-files-btn').click(() => {
        const selectedBucket = s3Manager.getSelectedBucket();  // Get selected bucket
        const selectedFiles = s3Manager.getSelectedFiles();  // Get selected files

        // Call the downloadFiles method from S3Manager
        s3Manager.downloadFiles(selectedBucket, selectedFiles);
    });



  });