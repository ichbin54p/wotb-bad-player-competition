function verify_score(id){
    alert("You don't have permissions to verify " + id)
}
function delete_score(id){
    alert("You don't have permissions to delete " + id)
}

if (localStorage.getItem("badges").split(" ").includes("Admin") || localStorage.getItem("badges").split(" ").includes("Moderator")) {
    verify_score = function(id){
        fetch(`/admin/api/score/${id}`, {method: "POST", headers: {username: localStorage.getItem("username"), password: localStorage.getItem("password")}}).then(function(r){if (r.ok){return r.text()} else {return false}}).then(function(data){
            if (data){
                switch (parseInt(data)){
                    case 0:
                        alert("Successfully verified score")
                        break
                    case 1:
                        alert("Your account doesn't exist")
                        break
                    case 2:
                        alert("Authorization error")
                        break
                    case 3:
                        alert("This score doesn't exist")
                        break
                }
            } else {
                alert("There was an error sending your request")
            }
        })
    }
    delete_score = function(id){
        fetch(`/admin/api/score/${id}`, {method: "DELETE", headers: {username: localStorage.getItem("username"), password: localStorage.getItem("password")}}).then(function(r){if (r.ok){return r.text()} else {return false}}).then(function(data){
            if (data){
                switch (parseInt(data)){
                    case 0:
                        alert("Successfully deleted score")
                        break
                    case 1:
                        alert("Your account doesn't exist")
                        break
                    case 2:
                        alert("Authorization error")
                        break
                    case 3:
                        alert("This score doesn't exist")
                        break
                }
            } else {
                alert("There was an error sending your request")
            }
        })
    }
}