$(document).ready(function() {
    // Fetch and populate bucket list when the page loads
    $.ajax({
        url: '/get_buckets',
        type: 'GET',
        success: function(data) {
            $('#bucket-list').empty();
            data.buckets.forEach(function(bucket) {
                $('#bucket-list').append(
                    `<li class="list-group-item" id="bucket-${bucket}">
                        <input type="radio" name="bucket" value="${bucket}" class="mr-2 bucket-radio"> 
                        ${bucket}
                     </li>`
                );
            });
        },
        error: function(error) {
            console.error("Error fetching buckets:", error);
        }
    });

    // Enable delete bucket button when a bucket is selected
    $(document).on('change', '.bucket-radio', function() {
        $('#delete-bucket-btn').prop('disabled', false);
        const selectedBucket = $('input[name="bucket"]:checked').val();
        $('#selected-bucket').text(selectedBucket);

        // Fetch files in the selected bucket
        $.ajax({
            url: '/get_files',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ bucket: selectedBucket }),
            success: function(data) {
                $('#file-list').empty();
                data.files.forEach(function(file) {
                    $('#file-list').append(
                        `<li class="list-group-item" id="file-${file}">
                            <input type="checkbox" name="file" value="${file}" class="mr-2 file-checkbox"> 
                            ${file}
                         </li>`
                    );
                });
                $('#delete-files-btn').prop('disabled', true);  // Disable file delete button initially
            },
            error: function(error) {
                console.error("Error fetching files:", error);
            }
        });
    });

    // Handle bucket deletion without reloading the page
    $('#delete-bucket-btn').click(function() {
        const selectedBucket = $('input[name="bucket"]:checked').val();
        if (selectedBucket) {
            if (confirm(`Are you sure you want to delete the bucket '${selectedBucket}'?`)) {
                $.ajax({
                    url: '/delete_bucket',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ bucket: selectedBucket }),
                    success: function() {
                        alert('Bucket deleted successfully.');
                        // Remove the deleted bucket from the UI
                        $(`#bucket-${selectedBucket}`).remove();
                        $('#file-list').empty();  // Clear the file list
                        $('#selected-bucket').text('None');  // Reset selected bucket
                        $('#delete-bucket-btn').prop('disabled', true);  // Disable delete button
                    },
                    error: function(error) {
                        console.error("Error deleting bucket:", error);
                    }
                });
            }
        }
    });

    // Handle file deletion without reloading the page
    $('#delete-files-btn').click(function() {
        const selectedBucket = $('input[name="bucket"]:checked').val();
        const selectedFiles = $('input[name="file"]:checked').map(function() {
            return this.value;
        }).get();

        if (selectedFiles.length > 0 && selectedBucket) {
            if (confirm(`Are you sure you want to delete the selected files?`)) {
                $.ajax({
                    url: '/delete_files',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ bucket: selectedBucket, files: selectedFiles }),
                    success: function() {
                        alert('Files deleted successfully.');
                        // Remove the deleted files from the UI
                        selectedFiles.forEach(function(file) {
                            $(`#file-${file}`).remove();  // Remove the file from the DOM
                        });
                        $('#delete-files-btn').prop('disabled', true);  // Disable delete button after deletion
                    },
                    error: function(error) {
                        console.error("Error deleting files:", error);
                    }
                });
            }
        }
    });

    // Enable delete files button when files are selected
    $(document).on('change', '.file-checkbox', function() {
        if ($('.file-checkbox:checked').length > 0) {
            $('#delete-files-btn').prop('disabled', false);
        } else {
            $('#delete-files-btn').prop('disabled', true);
        }
    });
});
