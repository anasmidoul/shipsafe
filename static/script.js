    document.getElementById("copy-api-key").addEventListener("click", function() {
        const apiKey = document.getElementById("api-key").textContent;
        navigator.clipboard.writeText(apiKey)
            .then(function() {
                const element = document.getElementById("copy-api-key");
                element.textContent = "Copied!";
                setTimeout(function() {
                element.textContent = "Copy API Key";
            }, 2000);
            })
            .catch(function(error) {
                console.log(error);
        });
    });

    const forms = document.querySelectorAll(".delete-flag");
        forms.forEach(function(form) {
            form.addEventListener("submit", function(event) {
                const confirmed = confirm("Are you sure you want to delete this flag?");
                if (!confirmed) {
                    event.preventDefault();
                }
            })
    });

    const toggleForms = document.querySelectorAll(".toggle-flag");
        toggleForms.forEach(function(form) {
            form.addEventListener("submit", function(event) {
                    event.preventDefault();
                    const url = form.action;
                    fetch(url, {
                        method: "POST"
                    })
                    .then(function(response) {
                        if (!response.ok) {
                            throw new Error("Request failed");
                        }
                        return response.json();
                    })
                    .then(function(data) {
                        const button = form.querySelector("button");

                        if (data.enabled === 1) {
                            button.textContent = "Disable";

                        } else {
                            button.textContent = "Enable";
                        }
                    })
                    .catch(function(error) {
                        alert("Something went wrong. Please try again.");
                    });
                    });
                });