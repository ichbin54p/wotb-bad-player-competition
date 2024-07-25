scores_element = document.getElementById("scores")

function sort_scores(){
    fetch("/api/score/scores").then(function(r){if (r.ok){try {return r.json()} catch(error){alert(error); console.error(); return false}} else {console.log(r); return false}}).then(function(data){
        scores = data

        switch (document.getElementById("sort").value){
            case "oldest":
                scores.sort(function(a, b){
                    return a.id - b.id
                })
                break;
            case "newest":
                scores.sort(function(a, b){
                    return b.id - a.id
                })
                break;
            case "score":
                scores.sort(function(a, b){
                    return b.id - a.id
                })
                break;
        }

        for (i = 0; i < scores.length; i++){
            switch (parseInt(document.getElementById("unverified").value)){
                case 1:
                    if (!scores[i].verified){
                        scores.splice(i, 1)
                    }
                    break
                case 2:
                    if (scores[i].verified){
                        scores.splice(i, 1)
                    }
                    break
                case 3:
                    break
            }
        }

        document.getElementById("scores").innerHTML = ""
        
        for (i = 0; i < scores.length; i++){
            document.getElementById("scores").innerHTML += `<div class=\"score\"><img src=\"/score/image/${scores[i].id}\"><h2><a href=\"/score/view/${scores[i].id}\">${scores[i].score} - ${scores[i].player}</a></h2><a href=\"/account/view/${scores[i].username}\">${scores[i].username}</a></div>`
        }
    })
}

sort_scores()

// document.getElementById("sort-scores").onclick = sort_scores()