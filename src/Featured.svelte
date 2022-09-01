<script>
    export let title;
    export let line;
    export let info;
    export let plot;
    export let img;
    export let imdbID;
    export let kind;
    //var inFavorites = false;
    //var inPlaylist = false;
    var favsSign = "";
    var plSign = "";
    var favsBTN = "";
    var plBTN = "";

    const handleFavorites = () => {
        const imdbID = favsBTN.dataset.id;

        if (favsBTN.innerText.includes("+")) {
            console.log("Adding ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/addToFavorites/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { favsSign = "-"; }
            };
            xhr.send();
        } else if (favsBTN.innerText.includes("-")) {
            console.log("Removing ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/removeFromFavorites/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { favsSign = "+"; }
            };
            xhr.send();
        } else { console.log("Unknown button state"); }

    }


    const handlePlaylist = () => {
        const playlist = document.getElementById("pl");
        const imdbID = playlist.dataset.id;

        if (playlist.innerText.includes("+")) {
            console.log("Adding ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/addToPlaylist/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { plSign = "-"; }
            };
            xhr.send();
        } else if (playlist.innerText.includes("-")) {
            console.log("Removing ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/removeFromPlaylist/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { plSign = "+"; }
            };
            xhr.send();
        } else { console.log("Unknown button state"); }
    }

    const onloadFavorites = () => {
        const favs = document.getElementById("favs");
        const imdbID = favs.dataset.id;
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/isInFavorites/" + imdbID, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (xhr.responseText.match(/Movie found in favorites/)) {
                    favsSign = "-"
                } else {
                    favsSign = "+"
                }
            }
        };
        xhr.send();
    }

    const onloadPlaylist = () => {
        const playlist = document.getElementById("pl");
        const imdbID = playlist.dataset.id;
        let xhr2 = new XMLHttpRequest();
        xhr2.open("GET", "/api/isInPlaylist/" + imdbID, true);
        xhr2.onreadystatechange = function() {
         if (xhr2.readyState == 4 && xhr2.status == 200) {
                if (xhr2.responseText.match(/Movie found in playlist/)) {
                    plSign = "-";
                } else {
                    plSign = "+";
                }
            }
        };
        xhr2.send();
    }

    const play = () => {
        const pb = document.getElementById("playButton")
        let url = `/play/${pb.dataset.id}/?kind=${pb.dataset.kind}`
        location = url
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
            <a data-id="{ imdbID }" id="playButton" class="bgRed" on:click={() => play()}>Play</a>
            <a bind:this={favsBTN} data-id="{ imdbID }" id="favs" on:click={() => handleFavorites()} use:onloadFavorites>{favsSign} Favorites</a>
            <a bind:this={plBTN} data-id="{ imdbID }" data-kind="{ kind }" id="pl" on:click={() => handlePlaylist()} use:onloadPlaylist>{plSign} Playlist</a>
        </div>
    </div>
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
        padding-left: 5%;
        padding-right: 5%;
        text-decoration: none;
        color: white;
        padding-top: .8%;
        padding-bottom: .8%;
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