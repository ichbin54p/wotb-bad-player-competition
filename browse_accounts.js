fetch("/api/account/accounts").then(function(r){if (r.ok){try {return r.json()} catch (error){alert(error); console.log(error); return false}} else {return false}}).then(function(data){
    if (data){
        data = data.sort(function(a, b){
            return b.priority - a.priority
        })
        for (i = 0; i < data.length; i++){
            badges = data[i].badges.split(" ")
            if (badges.includes("Admin")) {
                username = "[Admin] " + data[i].username
            } else if (badges.includes("Moderator")) {
                username = "[Moderator] " + data[i].username
            } else {
                username = data[i].username
            }
            console.log(badges)
            document.getElementById("accounts").innerHTML += "<h2><a href=\"/account/view/" + data[i].username + "\">" + username + "</a></h2>"
        }
    } else {
        alert("There was an error loading users... Please check the console or contact 54p")
    }
})