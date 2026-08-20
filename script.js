// 🌙 Dark / Light Mode

function toggleTheme() {

    document.body.classList.toggle(
        "light-mode"
    );

    const button =
        document.getElementById(
            "themeButton"
        );


    if (
        document.body.classList.contains(
            "light-mode"
        )
    ) {

        button.textContent =
            "🌙 Dark Mode";

    } else {

        button.textContent =
            "☀️ Light Mode";

    }

}



// 🐍 Talk to Python

function talkToPython() {

    const input =
        document.getElementById(
            "nameInput"
        );


    const name =
        input.value.trim();


    if (name === "") {

        alert(
            "⚠️ Please enter your name."
        );

        return;

    }


    fetch(
        "/api/hello?name=" +
        encodeURIComponent(name)
    )

        .then(function(response) {

            return response.json();

        })

        .then(function(data) {

            alert(
                data.message
            );

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
    document.querySelector(
        ".contact-form"
    );


if (contactForm) {

    contactForm.addEventListener(
        "submit",
        function(event) {

            event.preventDefault();


            const name =
                contactForm.querySelector(
                    'input[type="text"]'
                ).value;


            const email =
                contactForm.querySelector(
                    'input[type="email"]'
                ).value;


            const message =
                contactForm.querySelector(
                    "textarea"
                ).value;


            const contactData = {

                name: name,

                email: email,

                message: message

            };


            fetch(
                "/api/contact",
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
