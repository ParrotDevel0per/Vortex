<script>
    export let title;
    export let line;
    export let info;
    export let plot;
    export let img;
    export let imdbID;



    const isInFavs = (id) => {
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/isInFavorites/" + id, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (xhr.responseText.match(/Movie found in favorites/)) { return true; }
                return false
            }
        };
    }

    const isInPlaylist = (id) => {
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/isInPlaylist/" + id, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                if (xhr.responseText.match(/Movie found in playlist/)) { return true; }
                return false;
            }
        };
        xhr.send();
    }
</script>

<main>
    <div class="featured">
        <img class="featuredIMG" src="{ img }" alt="Featured">
        <div class="info">
            <h1>{ title }</h1>
            <h2>{ line }</h2>
            <h3>{ info }</h3>
            <h4>{ plot }</h4>
            <a class="bgRed" href="/">Play</a>
            <a id="favs" href="/">+ Favorites</a>
            <a id="playlist" href="/">+ Playlist</a>
        </div>
    </div>
</main>

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
    }
    .info > h1 {
        color: white;
        font-family: '28DayLater';
        font-size: 12em;
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
        width: 30%;
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
    .bgRed {
        background-color: red!important;
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