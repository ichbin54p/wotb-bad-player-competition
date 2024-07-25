document.getElementById("create_account").onclick = function(){
    username = document.getElementById("username")
    password = document.getElementById("password")
    discord_id = document.getElementById("discord-id")

    if (username.value == "" || password.value == ""){
        alert("Please fill in the input fields.")
    } else {
        fetch("/api/account/create", {method: "POST", headers: {username: username.value, discord: discord_id.value, password: password.value}}).then(function(r){if (r.ok){return r.text()} else {return 0}}).then(function(r){
            try {
                if (parseInt(r) == 1){
                    alert("Successfully created account, you can now sign in. Code: " + parseInt(r))
                    alert("Please contact an Administrator or Moderator if you want to be verified. If you do not know who to contact, just contact 54p (1098117095356641301)")
                    window.location.replace("/account/signin")
                } else {
                    alert("Error creating account, return code: " + parseInt(r))
                    if (parseInt(r) == 2){
                        alert("Account already exists")
                    } else if (parseInt(r) == 3){
                        alert("Your username, password or discord id is invalid. Password needs to be more than 5 characters and discord more than 7")
                    } else {
                        alert("Unkown error, please contact 54p")
                    }
                }
            } catch (error) {
                alert("Error creating account: " + error)
            }
        })
    }
}