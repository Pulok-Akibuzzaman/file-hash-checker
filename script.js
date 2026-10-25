const fileInput = document.getElementById("fileInput");
const algorithmSelect = document.getElementById("algorithm");
const calculateButton = document.getElementById("calculateButton");
const clearButton = document.getElementById("clearButton");
const copyButton = document.getElementById("copyButton");
const verifyButton = document.getElementById("verifyButton");

const fileInfo = document.getElementById("fileInfo");
const calculatedHash = document.getElementById("calculatedHash");
const expectedHash = document.getElementById("expectedHash");
const status = document.getElementById("status");

let selectedFile = null;

fileInput.addEventListener("change", () => {
    selectedFile = fileInput.files[0] || null;

    calculatedHash.value = "";
    expectedHash.value = "";
    copyButton.disabled = true;

    if (!selectedFile) {
        fileInfo.textContent = "No file selected.";
        setStatus("Select a file to begin.", "default");
        return;
    }

    fileInfo.textContent =
        `${selectedFile.name} — ${formatFileSize(selectedFile.size)}`;

    setStatus("File selected. Click Calculate Hash.", "default");
});

calculateButton.addEventListener("click", calculateFileHash);
clearButton.addEventListener("click", clearForm);
copyButton.addEventListener("click", copyHash);
verifyButton.addEventListener("click", verifyHash);

async function calculateFileHash() {
    if (!selectedFile) {
        setStatus("Please select a file first.", "warning");
        return;
    }

    if (!window.crypto?.subtle) {
        setStatus(
            "Web Crypto is unavailable. Open this page through GitHub Pages or HTTPS.",
            "error"
        );
        return;
    }

    calculateButton.disabled = true;
    copyButton.disabled = true;

    setStatus("Calculating hash...", "default");

    try {
        const fileBuffer = await selectedFile.arrayBuffer();
        const hashBuffer = await crypto.subtle.digest(
            algorithmSelect.value,
            fileBuffer
        );

        const hash = bufferToHex(hashBuffer);

        calculatedHash.value = hash;
        copyButton.disabled = false;

        setStatus("Hash calculated successfully.", "success");
    } catch (error) {
        console.error(error);
        setStatus("Could not calculate the file hash.", "error");
    } finally {
        calculateButton.disabled = false;
    }
}

async function copyHash() {
    const hash = calculatedHash.value.trim();

    if (!hash) {
        setStatus("Calculate a hash first.", "warning");
        return;
    }

    try {
        await navigator.clipboard.writeText(hash);
        setStatus("Hash copied to clipboard.", "success");
    } catch (error) {
        calculatedHash.select();
        document.execCommand("copy");
        setStatus("Hash copied to clipboard.", "success");
    }
}

function verifyHash() {
    const actual = calculatedHash.value.trim().toLowerCase();
    const expected = expectedHash.value
        .trim()
        .toLowerCase()
        .replace(/\s/g, "");

    if (!actual) {
        setStatus("Calculate the file hash first.", "warning");
        return;
    }

    if (!expected) {
        setStatus("Enter an expected hash first.", "warning");
        return;
    }

    if (actual === expected) {
        setStatus("MATCH: The hashes are identical.", "success");
    } else {
        setStatus("NO MATCH: The hashes are different.", "error");
    }
}

function clearForm() {
    selectedFile = null;
    fileInput.value = "";
    fileInfo.textContent = "No file selected.";
    calculatedHash.value = "";
    expectedHash.value = "";
    copyButton.disabled = true;

    setStatus("Select a file to begin.", "default");
}

function setStatus(message, type) {
    status.textContent = message;
    status.className = "status";

    if (type !== "default") {
        status.classList.add(type);
    }
}

function bufferToHex(buffer) {
    return Array.from(new Uint8Array(buffer))
        .map(byte => byte.toString(16).padStart(2, "0"))
        .join("");
}

function formatFileSize(bytes) {
    if (bytes === 0) {
        return "0 Bytes";
    }

    const units = ["Bytes", "KB", "MB", "GB", "TB"];
    const index = Math.floor(Math.log(bytes) / Math.log(1024));
    const size = bytes / Math.pow(1024, index);

    return `${size.toFixed(index === 0 ? 0 : 2)} ${units[index]}`;
}