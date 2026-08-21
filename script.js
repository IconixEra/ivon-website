const API_BASE = "https://ivon-website.onrender.com";

// 🌙 Dark / Light Mode
function toggleTheme() {
    document.body.classList.toggle("light-mode");

    const button = document.getElementById("themeButton");

    if (
        document.body.classList.contains("light-mode")
    ) {
        button.textContent = "🌙 Dark Mode";
    } else {
        button.textContent = "☀️ Light Mode";
    }
}


// 🐍 Talk to Python
function talkToPython() {

    const input = document.getElementById("nameInput");
    const name = input.value.trim();

    if (name === "") {
        alert("⚠️ Please enter your name.");
        return;
    }

    fetch(
        API_BASE +
        "/api/hello?name=" +
        encodeURIComponent(name)
    )

        .then(function(response) {

            if (!response.ok) {
                throw new Error(
                    "Server returned " +
                    response.status
                );
            }

            return response.json();
        })

        .then(function(data) {

            alert(data.message);

        })

        .catch(function(error) {

            console.log(error);

            alert(
                "❌ Python server is not connected."
            );

        });
}


// 📩 Contact Form
const contactForm =
    document.querySelector(".contact-form");


if (contactForm) {

    contactForm.addEventListener(
        "submit",
        function(event) {

            event.preventDefault();

            const name =
                contactForm.querySelector(
                    'input[type="text"]'
                ).value.trim();

            const email =
                contactForm.querySelector(
                    'input[type="email"]'
                ).value.trim();

            const message =
                contactForm.querySelector(
                    "textarea"
                ).value.trim();


            if (
                name === "" ||
                email === "" ||
                message === ""
            ) {

                alert(
                    "⚠️ Please fill in all fields."
                );

                return;
            }


            const contactData = {

                name: name,

                email: email,

                message: message

            };


            fetch(
                API_BASE + "/api/contact",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify(
                            contactData
                        )

                }
            )

                .then(function(response) {

                    if (!response.ok) {
                        throw new Error(
                            "Server returned " +
                            response.status
                        );
                    }

                    return response.json();

                })

                .then(function(data) {

                    alert(
                        "✅ " +
                        data.message
                    );

                    contactForm.reset();

                })

                .catch(function(error) {

                    console.log(error);

                    alert(
                        "❌ Could not send message."
                    );

                });

        }
    );

}
