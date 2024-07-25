fetch("/api/score/view?id=" + window.location.href.split("/")[window.location.href.split("/").length-1]).then(function(r){if (r.ok){try {return r.json()} catch (error){alert(error); console.log(error); return false}} else {return false}}).then(function(data){
    if (data.exists){
        document.getElementById("score").innerHTML = `<h1>${data.player} - Submitted by ${data.username}</h1><img style=\"width: 600px;\" src=\"/score/image/${data.id}\"><h2>Stats:</h2><h3>Score: <b class=\"output\">${data.score}</b><br>Battles: <b class=\"output\">${data.battles}</b><br>Winrate: <b class=\"output\">${data.winrate}%</b></h3>`
        if (data.verified){
            document.getElementById("score").innerHTML += "<h2 class=\"output\">Verified</h2>"
        } else {
            document.getElementById("score").innerHTML += "<h2 class=\"output\">Unverified</h2>"
        }
        if (localStorage.getItem("badges").split(" ").includes("Admin") || localStorage.getItem("badges").split(" ").includes("Moderator")) {
            document.getElementById("score").innerHTML += `<button onclick=\"verify_score(${data.id})\">Verify</button> <button onclick=\"delete_score(${data.id})\">Delete</button>`
        }
    } else {
        document.getElementById("score").remove()
        document.getElementById("main").innerHTML = "<h1>This score doesn't exist</h1>"
    }
})