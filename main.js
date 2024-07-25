logo = document.createElement("link")
logo.rel = "icon"
logo.type = "image/png"
logo.href = "/resource/logo_cropped.png"
document.head.appendChild(logo)

if (localStorage.getItem("username") != null && localStorage.getItem("password") != null){
    fetch("/api/account/badges", {headers: {username: localStorage.getItem("username"), password: localStorage.getItem("password")}}).then(function(r){if (r.ok){return r.text()} else {return false}}).then(function(data){
        if (data){
            localStorage.setItem("badges", data)
        }
    })
}