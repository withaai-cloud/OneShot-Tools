// File handling and conversion logic

let selectedFiles = [];

// Get elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const uploadForm = document.getElementById('uploadForm');
const convertBtn = document.getElementById('convertBtn');
const results = document.getElementById('results');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const resultsContent = document.getElementById('resultsContent');
const errorMessage = document.getElementById('errorMessage');
const statementYearSelect = document.getElementById('statementYear');

// Populate year dropdown (current year and 5 years back)
function populateYearDropdown() {
    const currentYear = new Date().getFullYear();
    
    for (let i = 0; i <= 5; i++) {
        const year = currentYear - i;
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        statementYearSelect.appendChild(option);
    }
}

// Initialize year dropdown on page load
populateYearDropdown();

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files).filter(file => file.name.endsWith('.pdf'));
    handleFiles(files);
});

// Click to upload - but not if clicking the button itself
uploadArea.addEventListener('click', (e) => {
    // Don't trigger if clicking the button (it has its own handler)
    if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
        return;
    }
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
});

// Handle selected files
function handleFiles(files) {
    files.forEach(file => {
        if (!selectedFiles.find(f => f.name === file.name)) {
            selectedFiles.push(file);
        }
    });
    
    updateFileList();
    updateConvertButton();
}

// Update file list display
function updateFileList() {
    if (selectedFiles.length === 0) {
        fileList.innerHTML = '';
        return;
    }
    
    fileList.innerHTML = '<div style="margin-bottom: 1rem;"><strong>Selected Files:</strong></div>';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';
        
        const fileIcon = document.createElement('span');
        fileIcon.className = 'file-icon';
        fileIcon.textContent = '📄';
        
        const fileDetails = document.createElement('div');
        
        const fileName = document.createElement('div');
        fileName.className = 'file-name';
        fileName.textContent = file.name;
        
        const fileSize = document.createElement('div');
        fileSize.className = 'file-size';
        fileSize.textContent = formatFileSize(file.size);
        
        fileDetails.appendChild(fileName);
        fileDetails.appendChild(fileSize);
        
        fileInfo.appendChild(fileIcon);
        fileInfo.appendChild(fileDetails);
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-file';
        removeBtn.textContent = 'Remove';
        removeBtn.type = 'button';
        removeBtn.onclick = () => removeFile(index);
        
        fileItem.appendChild(fileInfo);
        fileItem.appendChild(removeBtn);
        
        fileList.appendChild(fileItem);
    });
}

// Remove file from list
function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
    updateConvertButton();
}

// Update convert button state
function updateConvertButton() {
    convertBtn.disabled = selectedFiles.length === 0;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Handle form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (selectedFiles.length === 0) return;
    
    // Hide previous results/errors
    results.style.display = 'none';
    error.style.display = 'none';
    
    // Show loading
    loading.style.display = 'block';
    convertBtn.disabled = true;
    
    try {
        // Create FormData
        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append('files[]', file);
        });
        
        // Add invert option
        const invertAmounts = document.getElementById('invertAmounts').checked;
        formData.append('invert_amounts', invertAmounts);
        
        // Add output format option
        const outputFormat = document.querySelector('input[name="output_format"]:checked').value;
        formData.append('output_format', outputFormat);
        
        // Add statement year option
        const statementYear = document.getElementById('statementYear').value;
        formData.append('statement_year', statementYear);
        
        // Send request
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Conversion failed');
        }
        
        // Hide loading
        loading.style.display = 'none';
        
        // Show results
        displayResults(data);
        
    } catch (err) {
        loading.style.display = 'none';
        error.style.display = 'block';
        errorMessage.textContent = err.message;
        convertBtn.disabled = false;
    }
});

// Update button text when format changes
document.querySelectorAll('input[name="output_format"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        const btnText = document.getElementById('convertBtnText');
        if (e.target.value === 'excel') {
            btnText.textContent = 'Convert to Excel';
        } else {
            btnText.textContent = 'Convert to CSV';
        }
    });
});

// Display results
function displayResults(data) {
    resultsContent.innerHTML = '';
    
    // Helper function to trigger download from base64
    function downloadFile(filename, base64Data) {
        const link = document.createElement('a');
        link.href = 'data:application/octet-stream;base64,' + base64Data;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    
    if (data.multiple) {
        // Multiple files processed
        const summary = document.createElement('div');
        summary.className = 'result-file';
        summary.innerHTML = `
            <h4>Processed ${data.files.length} files</h4>
            <p class="result-stats">Total transactions extracted: ${data.total_transactions}</p>
        `;
        resultsContent.appendChild(summary);
        
        // Individual files
        data.files.forEach(file => {
            const fileResult = document.createElement('div');
            fileResult.className = 'result-file';
            
            const title = document.createElement('h4');
            title.textContent = file.original;
            fileResult.appendChild(title);
            
            const stats = document.createElement('p');
            stats.className = 'result-stats';
            stats.textContent = `${file.transactions} transactions`;
            fileResult.appendChild(stats);
            
            const downloadBtn = document.createElement('button');
            downloadBtn.className = 'btn btn-secondary';
            downloadBtn.textContent = 'Download File →';
            downloadBtn.onclick = () => downloadFile(file.output, data.file_data[file.output]);
            fileResult.appendChild(downloadBtn);
            
            resultsContent.appendChild(fileResult);
        });
        
        // Combined and ZIP download
        const downloadButtons = document.createElement('div');
        downloadButtons.className = 'download-buttons';
        
        const combinedBtn = document.createElement('button');
        combinedBtn.className = 'btn btn-primary';
        combinedBtn.textContent = '📊 Download Combined File';
        combinedBtn.onclick = () => downloadFile(data.combined, data.file_data[data.combined]);
        downloadButtons.appendChild(combinedBtn);
        
        const zipBtn = document.createElement('button');
        zipBtn.className = 'btn btn-primary';
        zipBtn.textContent = '📦 Download All (ZIP)';
        zipBtn.onclick = () => downloadFile(data.zip, data.file_data[data.zip]);
        downloadButtons.appendChild(zipBtn);
        
        resultsContent.appendChild(downloadButtons);
        
    } else {
        // Single file processed
        const fileResult = document.createElement('div');
        fileResult.className = 'result-file';
        fileResult.innerHTML = `
            <h4>Successfully converted!</h4>
            <p class="result-stats">${data.transactions} transactions extracted</p>
        `;
        resultsContent.appendChild(fileResult);
        
        const downloadButtons = document.createElement('div');
        downloadButtons.className = 'download-buttons';
        
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'btn btn-primary';
        downloadBtn.textContent = '📊 Download File';
        downloadBtn.onclick = () => downloadFile(data.file, data.file_data[data.file]);
        downloadButtons.appendChild(downloadBtn);
        
        resultsContent.appendChild(downloadButtons);
    }
    
    // Add "Convert More" button
    const convertMoreBtn = document.createElement('button');
    convertMoreBtn.className = 'btn btn-secondary';
    convertMoreBtn.textContent = 'Convert More Files';
    convertMoreBtn.style.marginTop = '1.5rem';
    convertMoreBtn.onclick = () => location.reload();
    resultsContent.appendChild(convertMoreBtn);
    
    results.style.display = 'block';
}
