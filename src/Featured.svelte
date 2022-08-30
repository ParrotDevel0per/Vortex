<script>
    export let title;
    export let line;
    export let info;
    export let plot;
    export let img;
    export let imdbID;

    const handleFavorites = () => {
        const favs = document.getElementById("favs");
        const imdbID = favs.dataset.id;

        if (favs.innerText.includes("+")) {
            console.log("Adding ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/addToFavorites/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    favs.innerText = "- Favorites";
                }
            };
            xhr.send();
        } else if (favs.innerText.includes("-")) {
            console.log("Removing ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/removeFromFavorites/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    favs.innerText = "+ Favorites";
                }
            };
            xhr.send();
        } else { console.log("Unknown button state"); }

    }


    const handlePlaylist = () => {
        const playlist = document.getElementById("pl");
        const imdbID = playlist.dataset.id;

        if (isShow) { return; }

        if (playlist.innerText.includes("+")) {
            console.log("Adding ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/addToPlaylist/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    playlist.innerText = "- Playlist";
                }
            };
            xhr.send();
        } else if (playlist.innerText.includes("-")) {
            console.log("Removing ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/removeFromPlaylist/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    playlist.innerText = "+ Playlist";
                }
            };
            xhr.send();
        } else { console.log("Unknown button state"); }
    }
</script>

<div class="featuredContainer">
    <div id="featured" class="featured">
        <img class="featuredIMG" src="{ img }" alt="Featured">
        <div id="featuredInfo" class="info">
            {#if title == "JOKER"}
            <h1 class="jokerFont">{ title }</h1>
            {:else}
            <h1>{ title }</h1>
            {/if}
            {#if line}
            <h2>{ line }</h2>
            {/if}
            {#if info}
            <h3>{ info }</h3>
            {/if}
            {#if plot}
            <h4>{ plot }</h4>
            {/if}
            <a data-id="{ imdbID }" id="play" class="bgRed" on:click={() => console.log("play")}>Play</a>
            <a data-id="{ imdbID }" id="favs" on:click={() => handleFavorites()}>+ Favorites</a>
            <a data-id="{ imdbID }" id="pl" on:click={() => handlePlaylist()}>+ Playlist</a>
        </div>
    </div>
    <script>
        
        
        const featuredInfo = document.getElementById("featuredInfo");
        var isShow = false;


        // Check if movie is in favourites
        const checker = () => {
            xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/isInFavorites/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    if (xhr.responseText.match(/Movie found in favorites/)) {
                        favs.innerText = "- Favorites";
                    } else {
                        favs.innerText = "+ Favorites";
                    }
                }
            };
            xhr.send();
            xhr2 = new XMLHttpRequest();
            xhr2.open("GET", "/api/isInPlaylist/" + imdbID, true);
            xhr2.onreadystatechange = function() {
                if (xhr2.readyState == 4 && xhr2.status == 200) {
                    if (xhr2.responseText.match(/Movie found in playlist/)) {
                        playlist.innerText = "- Playlist";
                    } else {
                        playlist.className = "+ Playlist";
                    }
                }
            };
            xhr2.send();
        }


    </script>
</div>

<style>
    @font-face {
        font-family: '28DayLater';
        src: url('/static/fonts/28DayLater.ttf');
    }

    @font-face {
        font-family: 'Bignoodletitling';
        src: url('/static/fonts/Bignoodletitling.ttf');
    }
    .featured {
        height: 100vh;
        width: 100vw;
        display: block;
        margin-bottom: 2vh;
        position: relative;
    }
    .info {
        float: left;
        position: absolute;
        left: 10%;
        top: 20%;
        z-index: 1000;
        padding: 5px;
        width: 30%;
        text-align: center;
    }
    .info > h1 {
        color: white;
        font-size: 4vw;
    }
    .jokerFont {
        font-family: '28DayLater';
        font-size: 10vw!important;
    }
    .info > h2 {
        color: white;
        font-family: 'Bignoodletitling';
        font-size: 3.3em;
    }
    .info > h3 {
        color: white;
        font-size: 1em;
        margin-left: 5%;
    }
    .info > h4 {
        color: #6d737a;
        width: 100%;
        font-size: .9em;
        margin-bottom: 2rem;
    }
    .info > a {
        background-color: #212121;
        display: inline;
        padding-left: 3%;
        padding-right: 3%;
        text-decoration: none;
        color: white;
        padding-top: .5%;
        padding-bottom: .5%;
        border-radius: 3px;
    }
    .info > a:hover {
        background-color: #6d737a;
        cursor: pointer;
    }
    .bgRed {
        background-color: red!important;
    }
    .bgRed:hover {
        background-color: #ff4444!important;
        cursor: pointer;
    }

    .featuredIMG {
        width: 100%;
        filter: brightness(20%);
    }
    @media screen and (max-width: 600px) {
        .featured {
            display: none;
        }
    }
    @media screen and (max-width: 992px) {
        .featured {
            display: none;
        }
    }
</style>