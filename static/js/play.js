const favs = document.getElementById("favs"); // fontawsome icon
const playlist = document.getElementById("pl"); // fontawsome icon
const showPlaylist = document.getElementById("showPlaylist"); // p tag
const plIcon = "fa-square-plus";
const favIcon = "fa-heart";
var isShow = false;

$("#showPlaylist").bind('paste', function(e) {
    $(this).attr("maxlength", "1000")
});
$("#showPlaylist").on("input", function() {
    $(this).attr("maxlength", "0")
});


// Check if movie is in favourites
window.addEventListener("load", function() {
    var url = window.location.href;
    if (url.includes("-")) {
        let id = url.split("/play/")[1].split("/")[0];
        let showURL = url.split("/play/")[0] + "/show/" + id + ".m3u";
        showPlaylist.innerText = showURL;
        isShow = true;
    }
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/isInFavorites/" + id, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            if (xhr.responseText.match(/Movie found in favorites/)) {
                favs.className = `fa-solid ${favIcon} icon fav`;
            } else {
                favs.className = `fa-regular ${favIcon} icon fav`;
            }
        }
    };
    xhr.send();
    xhr2 = new XMLHttpRequest();
    xhr2.open("GET", "/api/isInPlaylist/" + id, true);
    xhr2.onreadystatechange = function() {
        if (xhr2.readyState == 4 && xhr2.status == 200) {
            if (xhr2.responseText.match(/Movie found in playlist/)) {
                playlist.className = `fa-solid ${plIcon} icon pl`;
            } else {
                playlist.className = `fa-regular ${plIcon} icon pl`;
            }
        }
    };
    xhr2.send();
});

// Add or remove movie from favorites
favs.addEventListener("click", function() {
    if (favs.className.includes("fa-regular")) {
        console.log("Adding ...");
        xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/addToFavorites/" + id, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                favs.className = `fa-solid ${favIcon} icon fav`;
            }
        };
        xhr.send();
    } else if (favs.className.includes("fa-solid")) {
        console.log("Removing ...");
        xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/removeFromFavorites/" + id, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                favs.className = `fa-regular ${favIcon} icon fav`;
            }
        };
        xhr.send();
    } else {
        console.log("Unknown button state");
    }
});

// Add or remove movie from playlist
playlist.addEventListener("click", function() {
    if (playlist.className.includes("fa-regular")) {
        if (isShow) {
            showPlaylist.style.display = "block";
            playlist.className = `fa-solid ${plIcon} icon pl`;
            return;
        }
        console.log("Adding ...");
        xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/addToPlaylist/" + id, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                playlist.className = `fa-solid ${plIcon} icon pl`;
            }
        };
        xhr.send();
    } else if (playlist.className.includes("fa-solid")) {
        if (isShow) {
            showPlaylist.style.display = "none";
            playlist.className = `fa-regular ${plIcon} icon pl`;
            return;
        }
        console.log("Removing ...");
        xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/removeFromPlaylist/" + id, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                playlist.className = `fa-regular ${plIcon} icon pl`;
            }
        };
        xhr.send();
    } else {
        console.log("Unknown button state");
    }
});