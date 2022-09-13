window.addEventListener("load", () => {
    const canvas = document.querySelector("#canvas");
    const _input = document.querySelector("#input-form");
    const classes = document.getElementsByClassName("wordle-row");
    const numberOfGuesses = 6;
    
    const getRow = (word) => {
        for(let i = 0; i < classes.length; i++) {
            for(let node of classes[i].childNodes) {
                if (!node.innerText) return i;
            }
        }

        return -1;
    }

    const styleRow = async (word, wordOutline) => {
        let row = getRow(word);
        if(row != -1) {
            let cls = classes[row];
            for(let i = 0; i < 5; ++i) {
                switch(wordOutline[i]) {
                    case "G":
                        cls.childNodes[i].style.backgroundColor = "green";
                        cls.childNodes[i].innerText = word[i];
                        break;
                    case "O":
                        cls.childNodes[i].style.backgroundColor = "orange";
                        cls.childNodes[i].innerText = word[i];
                        break;
                    default:
                        cls.childNodes[i].style.backgroundColor = "red";
                        cls.childNodes[i].innerText = word[i];
                        break;
                }
            }
        }

        return row;
    }

     _input?.addEventListener("submit", async e => {

        e.preventDefault();
        let _word = _input.input?.value;
        _input.input.value = "";

        let parsed = await fetch("/api/todays-word", {
            method: "POST",
            body: JSON.stringify({"word": _word}),
            headers: {
                "Authorization": "SUPER SECRET ADMIN KEY",
            }
        }).then(res => res.text()).then(text => JSON.parse(text))

        let word = parsed?.word ?? "_____";
        let username = parsed?.username;

        let rowNum = await styleRow(_word, word);

        if(word === "GGGGG") {
            await fetch(`/api/award-point/${username}`, {
                method: "POST",
                headers: {
                    "Authorization": "SUPER SECRET ADMIN KEY",
                }
            })
            alert("You Won!");
            window.location.href = "/";
        } else if(rowNum === 5 && word != "GGGGG") {
            await fetch(`/api/award-loss/${username}`, {
                method: "POST",
                headers: {
                    "Authorization": "SUPER SECRET ADMIN KEY",
                }
            })
            setTimeout(() => {
                alert("You Lost!");
                window.location.href = "/";
            }, 300);
        }
    })

    const generateBoard = () => {
        for(let i = 0; i < numberOfGuesses; i++) {
            let row = document.createElement("div");
            row.classList.add("wordle-row");
            row.id = `row-${i}`;

            for(let j = 0; j < 5; j++) {
                let wordBox = document.createElement("div");
                wordBox.classList.add("box");
                row.appendChild(wordBox);
            }

            canvas.appendChild(row);
        }
    }

    generateBoard();
})