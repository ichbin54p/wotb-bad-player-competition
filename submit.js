if (localStorage.getItem("username") == null){
    document.getElementById("username").innerText = "Please log in or create an account"
} else {
    document.getElementById("username").innerText = localStorage.getItem("username")
}

let screenshot_proof = document.getElementById("screenshot-proof")
let has_screenshot_proof = false

document.onpaste = function(event){
    let items = (event.clipboardData || event.origonalEvent.clipboardData).items
    for (i = 0; i < items.length; i++){
        if (items[i].kind == "file"){
            has_screenshot_proof = true

            let file = items[i].getAsFile()
            let reader = new FileReader()

            reader.onload = function(e){
                document.getElementById("screenshot-proof-image").innerHTML = "<img style=\"width: 790px; height: 400px;\" id=\"screenshot_image\" src=\"" + e.target.result + "\">"
            }

            reader.readAsDataURL(file)
        }
    }
}

if (localStorage.getItem("username") != null && localStorage.getItem("password") != null){
    document.getElementById("submit").onclick = function(){
        if (has_screenshot_proof && document.getElementById("player").value.length > 2){            
            fetch("/api/score/create", {headers: {username: localStorage.getItem("username"), password: localStorage.getItem("password"), player: document.getElementById("player").value}, method: "POST", body: document.getElementById("screenshot_image").src}).then(function(r){if (r.ok){try {return r.json()} catch(error){console.log(error); alert(error)}} else {return 0}}).then(function(data){
                if (data){
                    switch (data.code) {
                        case 0:
                            alert("You have already added this player")
                            break;
                        case 1:
                            alert("Your account does not exist")
                            break;
                        case 2:
                            alert("Authorization error...")
                            break;
                        case 3:
                            alert("There was an error processing the image")
                            break;
                        case 4:
                            alert("Successfully submitted score.")
                            break;
                        case 5:
                            alert("This player does not exist")
                            break;
                    }
                } else {
                    alert("There was an internal error, please check console")
                }
            })
        } else {
            alert("Please fill in the fields.")
        }
    }
} else {
    alert("Error: you are not logged in, please login or create an account")
}