window.addEventListener("load", () => {
    const btn = document.querySelector("#delete-account-btn");

    btn.addEventListener("click", () => {
        const deleteDiv = document.querySelector("#delete-account-container");
        const accepttBtn = document.getElementById("accept-btn");

        if(accepttBtn == null) {
            const text = document.createElement("h5");
            text.innerText = "Are You Sure You'd Like To Delete Your Account?";
            text.style.textAlign = "center";

            const acceptDiv = document.createElement("div");
            const denyDiv = document.createElement("div");
            const acceptBtn = document.createElement("button");
            const denyBtn = document.createElement("button");
        
            acceptBtn.innerText = "Yes";
            acceptBtn.className = "btn btn-dark btn-primary";
            acceptBtn.id = "accept-btn";
            denyBtn.innerText = "No";
            denyBtn.className = "btn btn-dark btn-primary";
            denyBtn.id = "deny-btn";

            acceptBtn.addEventListener("click", () => {
                window.location.href = "/delete-account";
            });

            denyBtn.addEventListener("click", () => {
                for(let elem of [acceptBtn, denyBtn, acceptDiv, denyDiv, text]) {
                    elem.remove();
                }
            });

            acceptDiv.appendChild(acceptBtn);
            denyDiv.appendChild(denyBtn);

            deleteDiv.append(text, acceptDiv, denyDiv);
        }
    })
})