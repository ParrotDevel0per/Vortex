<script>
    export let title;
    export let line;
    export let info;
    export let plot;
    export let imdbID;
    export let kind;
    export var inFavorites;
    export var inPlaylist;

    if (id) imdbID = id;

    var favsBTN = "";
    var plBTN = "";
    var playBTN = "";

    const handleFavorites = () => {
        const imdbID = favsBTN.dataset.id;

        if (favsBTN.innerText.includes("+")) {
            console.log("Adding ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/addToFavorites/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { inFavorites = true; }
            };
            xhr.send();
        } else if (favsBTN.innerText.includes("-")) {
            console.log("Removing ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/removeFromFavorites/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { inFavorites = false; }
            };
            xhr.send();
        } else { console.log("Unknown button state"); }

    }


    const handlePlaylist = () => {
        const imdbID = plBTN.dataset.id;

        if (plBTN.innerText.includes("+")) {
            console.log("Adding ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/addToPlaylist/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { inPlaylist = true; }
            };
            xhr.send();
        } else if (plBTN.innerText.includes("-")) {
            console.log("Removing ...");
            let xhr = new XMLHttpRequest();
            xhr.open("GET", "/api/removeFromPlaylist/" + imdbID, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) { inPlaylist = false; }
            };
            xhr.send();
        } else { console.log("Unknown button state"); }
    }

    const play = () => {
        let url = `/watch/${playBTN.dataset.id}/`
        if (kind) url += `?kind=${kind}`;
        location = url
    }
</script>

<div class="featuredContainer">
    <div id="featured" class="featured">
        <img class="featuredIMG" src={imdbID ? `/api/banner/${ imdbID }?do=show` : ""} alt="Featured">
        <div id="featuredInfo" class="info">
            <h1 class={title.toLowerCase() == "joker" ? "jokerFont" : "normalFont" }>{@html title.replace(": ", ": <br />") }</h1>

            {#if line}
            <h2>{ line }</h2>
            {/if}
            {#if info}
            <h3>{ info }</h3>
            {/if}
            {#if plot}
            <h4>{ plot }</h4>
            {/if}
            
            {#if imdbID && kind}
                <a bind:this={playBTN} data-id="{ imdbID }" id="playButton" class="bgRed" on:click={() => play()}>Play</a>
                <a bind:this={favsBTN} data-id="{ imdbID }" id="favs" on:click={() => handleFavorites()}>{inFavorites ? "-" : "+"} Favorites</a>
                {#if kind != "show"}
                    <a bind:this={plBTN} data-id="{ imdbID }" id="pl" on:click={() => handlePlaylist()}>{inPlaylist ? "-" : "+"} Playlist</a>
                {/if}
            {/if}
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
    @font-face {
        font-family: 'VanguardCF-Regular';
        src: url('/static/fonts/VanguardCF/VanguardCF-Regular.otf');
    }
    /* input, */
    /*
    input {
        padding-left: 0.5vh;
        padding-bottom: 0.5vh;
        padding-left: 0px;
        padding-right: 0px;
        text-align: center!important;
        width: 10%!important;
    }
    input:focus {
        outline:none !important;
    }
    */
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
        width: 40%;
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
    .normalFont {
        font-family: 'VanguardCF-Regular';
        font-size: 5vw !important;
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
        padding-left: 7%;
        padding-right: 7%;
        text-decoration: none;
        color: white;
        padding-top: 1.2%;
        padding-bottom: 1.2%;
        border-radius: 3px;
    }
    .info > a:hover {
        background-color: #6d737a;
        cursor: pointer;
    }
    .bgRed {
        background-color: blue!important;
    }
    .bgRed:hover {
        background-color: #1703cc!important;
        cursor: pointer;
    }

    .featuredIMG {
        width: 100%;
        filter: brightness(20%);
        object-fit: cover;
        height: 200%;
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