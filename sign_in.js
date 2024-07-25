document.getElementById("sign_in").onclick = function(){
    username = document.getElementById("username")
    password = document.getElementById("password")

    if (username.value == "" || password.value == ""){
        alert("Please fill in the input fields.")
    } else {
        fetch("/api/account/login", {method: "POST", headers: {username: username.value, password: password.value}}).then(function(r){if (r.ok){return r.text()} else {return 0}}).then(function(r){
            try {
                if (parseInt(r) == 1){
                    localStorage.setItem("username", username.value)
                    localStorage.setItem("password", password.value)
                    alert("Successfully signed in, code: " + parseInt(r))
                    window.location.replace("/")
                } else {
                    alert("Error signing in, code: " + parseInt(r))
                }
            } catch (error) {
                console.log(error)
                alert("Error creating account: " + error)
            }
        })
    }
}