/**
 * Language Learning App - Main JS
 * --------------------------------
 * Handles module button interactions
 * and communicates with backend API.
 */

/**
 * Sends module request to backend
 * @param {number} id - Module number (1–6)
 */
function requestModule(id) {

    // Call backend API endpoint
    fetch(`/api/modules/${id}`)
        .then(response => response.json())
        .then(data => {
            // Update message field with backend response
            document.getElementById("message").textContent = data.message;
        })
        .catch(error => {
            // Handle errors gracefully
            document.getElementById("message").textContent = "Error contacting server";
            console.error("API Error:", error);
        });
}