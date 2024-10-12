$(document).ready(function() {
    // Usage Example: Initialize the S3Manager
    const s3Manager = new S3Manager();

    // Ensure the run-algs-btn exists before adding the event listener
    const runAlgsBtn = document.getElementById('run-algs-btn');
    
    if (runAlgsBtn) {
        runAlgsBtn.addEventListener('click', function() {
            // Initialize selectedFiles dictionary
            const selectedFiles = {};

            // Collect the bucket names and files from the first card
            const bucketElements = document.querySelectorAll('[id^="bucket-"]');
            bucketElements.forEach(bucketElement => {
                // Ensure the ID contains a hyphen and skip any elements that are not buckets (like 'bucket-files')
                const bucketIdParts = bucketElement.id.split('-');
                if (bucketIdParts.length < 2 || bucketIdParts[1] === 'files') {
                    console.warn('Skipping element with unexpected ID or files:', bucketElement.id);
                    return;
                }

                const bucketId = bucketIdParts[1];  // Extract the unique part of the ID

                // Debugging: Check the bucketId
                console.log('Bucket ID:', bucketId);

                // Try to find the bucket name element and log it
                const bucketNameElement = document.getElementById(`bucket-name-${bucketId}`);
                console.log('Bucket Name Element:', bucketNameElement);

                if (bucketNameElement) {
                    const bucketName = bucketNameElement.textContent.trim();
                    console.log('Bucket Name:', bucketName);

                    // Collect the files associated with this bucket
                    const fileElements = document.querySelectorAll(`#bucket-files-${bucketId} li`);
                    const files = Array.from(fileElements).map(fileElement => fileElement.textContent.trim());

                    // If files exist, add them to the selectedFiles object
                    if (files.length > 0) {
                        selectedFiles[bucketName] = files;
                    }
                } else {
                    console.log(`Bucket name element not found for bucket ID: ${bucketId}`);
                }
            });

            // Log final selected files to ensure they're captured correctly
            console.log('Final Selected Files:', selectedFiles);

            // Now get the selected algorithms
            const selectedAlgorithms = [];
            document.querySelectorAll('input[name="algorithms"]:checked').forEach(checkbox => {
                selectedAlgorithms.push(checkbox.value);
            });

            // Log the selected algorithms to ensure they're captured correctly
            console.log('Selected Algorithms:', selectedAlgorithms);

            // Show final data in the confirmation modal
            const dataToSend = {
                files: selectedFiles,
                algorithms: selectedAlgorithms
            };

            console.log('Data to send:', dataToSend);

            // Populate the modal with the selected data
            const selectedItemsList = document.getElementById('selectedItemsList');
            selectedItemsList.innerHTML = ''; // Clear previous content

            // List selected files
            if (Object.keys(selectedFiles).length > 0) {
                const filesList = document.createElement('li');
                filesList.innerHTML = `<strong>Selected Files:</strong> ${Object.entries(selectedFiles).map(([bucket, files]) => `${bucket}: ${files.join(', ')}`).join('<br>')}`;
                selectedItemsList.appendChild(filesList);
            } else {
                console.log('No files selected.');
            }

            // List selected algorithms
            if (selectedAlgorithms.length > 0) {
                const algosList = document.createElement('li');
                algosList.innerHTML = `<strong>Selected Algorithms:</strong> ${selectedAlgorithms.join(', ')}`;
                selectedItemsList.appendChild(algosList);
            } else {
                console.log('No algorithms selected.');
            }

            // Show the modal
            $('#confirmationModal').modal('show');

            // Ensure confirm button only has one event listener
            document.getElementById('confirm-btn').addEventListener('click', function() {
                // Send the data to the backend
                fetch('/process_data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dataToSend)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    // Hide the modal after confirmation
                    $('#confirmationModal').modal('hide');
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }, { once: true }); // Ensure event listener is only added once
        });
    } else {
        console.error('Run button not found!');
    }
});
