fetch("/api/account/view?username=" + window.location.href.split("/")[window.location.href.split("/").length-1]).then(function(r){if (r.ok){try {return r.json()} catch (error){alert(error); console.log(error); return false}} else {return false}}).then(function(data){
    if (data.exists){
        document.getElementById("username").innerText = data.username
        document.getElementById("discord").innerText = data.discord
        
        badges = data.badges.split(" ")

        for (i = 0; i < badges.length; i++){
            badge = document.createElement("span")
            badge.classList.add("badge")
            badge.innerText = badges[i]
            document.getElementById("badges").appendChild(badge)
            document.getElementById("badges").innerHTML += "<b style=\"color: rgba(0, 0, 0, 0);\">##</b>"
        }
    } else {
        document.getElementById("account").remove()
        document.getElementById("main").innerHTML = "<h1>This account doesn't exist</h1>"
    }
})