const API_URL = "http://127.0.0.1:8000";


// --------------------------------------------------
// MODE SWITCHING
// --------------------------------------------------

function showTextMode() {

    document
        .getElementById("textMode")
        .classList.remove("hidden");

    document
        .getElementById("fileMode")
        .classList.add("hidden");

    document
        .getElementById("textTab")
        .classList.add("active");

    document
        .getElementById("fileTab")
        .classList.remove("active");
}


function showFileMode() {

    document
        .getElementById("textMode")
        .classList.add("hidden");

    document
        .getElementById("fileMode")
        .classList.remove("hidden");

    document
        .getElementById("textTab")
        .classList.remove("active");

    document
        .getElementById("fileTab")
        .classList.add("active");
}


// --------------------------------------------------
// UI HELPERS
// --------------------------------------------------

function showLoading() {

    document
        .getElementById("loading")
        .classList.remove("hidden");

}


function hideLoading() {

    document
        .getElementById("loading")
        .classList.add("hidden");

}


function showError(message) {

    const error =
        document.getElementById("error");

    error.textContent = message;

    error.classList.remove("hidden");
}


function hideError() {

    document
        .getElementById("error")
        .classList.add("hidden");
}


// --------------------------------------------------
// TEXT ANALYSIS
// --------------------------------------------------

async function analyzeText() {

    hideError();

    const text =
        document
            .getElementById("textInput")
            .value
            .trim();


    if (!text) {

        showError(
            "Please enter some text."
        );

        return;
    }


    showLoading();


    try {

        const response =
            await fetch(
                `${API_URL}/detect`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Analysis failed."
            );
        }


        displayResults(
            data.result
        );

    }
    catch (error) {

        showError(
            error.message
        );

    }
    finally {

        hideLoading();

    }
}


// --------------------------------------------------
// FILE ANALYSIS
// --------------------------------------------------

async function analyzeFile() {

    hideError();


    const fileInput =
        document.getElementById(
            "fileInput"
        );


    if (!fileInput.files.length) {

        showError(
            "Please select a PDF, DOCX, or TXT file."
        );

        return;
    }


    const file =
        fileInput.files[0];


    const allowedTypes = [
        ".pdf",
        ".docx",
        ".txt"
    ];


    const filename =
        file.name.toLowerCase();


    const valid =
        allowedTypes.some(
            extension =>
                filename.endsWith(extension)
        );


    if (!valid) {

        showError(
            "Only PDF, DOCX and TXT files are supported."
        );

        return;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    showLoading();


    try {

        const response =
            await fetch(
                `${API_URL}/analyze-file`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "File analysis failed."
            );
        }


        displayResults(
            data.result
        );

    }
    catch (error) {

        showError(
            error.message
        );

    }
    finally {

        hideLoading();

    }
}


// --------------------------------------------------
// DISPLAY RESULTS
// --------------------------------------------------

function displayResults(result) {

    document
        .getElementById("results")
        .classList.remove("hidden");


    document
        .getElementById("prediction")
        .textContent =
            result.overall_prediction;


    document
        .getElementById("confidence")
        .textContent =
            `${result.average_confidence}%`;


    document
        .getElementById("wordCount")
        .textContent =
            result.total_words;


    document
        .getElementById("chunkCount")
        .textContent =
            result.total_chunks;


    const chunkContainer =
        document.getElementById(
            "chunkResults"
        );


    chunkContainer.innerHTML = "";


    result.chunks.forEach(
        chunk => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "chunk-item";


            item.innerHTML = `
                <div>
                    <strong>
                        Chunk ${chunk.chunk}
                    </strong>
                </div>

                <div class="chunk-label">
                    ${chunk.label}
                    —
                    ${chunk.confidence}%
                </div>

                <div class="chunk-text">
                    ${escapeHtml(chunk.text)}
                </div>
            `;


            chunkContainer.appendChild(
                item
            );

        }
    );


    document
        .getElementById("results")
        .scrollIntoView({
            behavior: "smooth"
        });
}


// --------------------------------------------------
// HTML ESCAPE
// --------------------------------------------------

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent = text;

    return div.innerHTML;
}