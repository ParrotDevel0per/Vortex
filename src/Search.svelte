<script>
import Nav from "./Nav.svelte";
import axios from 'axios';

//var search = "";
//var results = {};

var term = localStorage.getItem("lastQuery") ? localStorage.getItem("lastQuery") : "";

function preloadImage(url) {
		var img=new Image();
		img.src=url;
}
preloadImage("/static/img/loading.gif")

/*
const searchEngine = () => {
    const searchTerm = search.value.toLowerCase();
    if (searchTerm.length >= 3) {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                var resp = JSON.parse(xmlHttp.responseText);
                resp = resp["results"];
                if (resp == undefined) { return; }
                results = resp;
            }
        }
        xmlHttp.open("GET", "/api/search/" + searchTerm, true);
        xmlHttp.setRequestHeader('Accept', 'application/json');
        xmlHttp.send(null);
    } else {
      results = {};
    }
}
*/
const view = (id) => {
  preloadImage(`/api/banner/${id}?do=show`);
  location = `/?showG=false&id=${id}`;
}
</script>

<main>
    <Nav active="search" />
    <input
        bind:value={term}
        on:keyup={() => localStorage.setItem("lastQuery", term)}
        type="text"
        placeholder="Search ..."
    >

    {#if term}
      <div id="grid">
        {#await axios.get("/api/search/" + term, {transformResponse: (res) => { return JSON.parse(res); }, responseType: 'json'})}
          <p style="display: none;">Loading ...</p>
        {:then resp}
          {#each Object.values(resp.data.results) as r}
          <div class="item" on:click={() => view(r.id)}>
              <img src="/api/poster/{ r.id }?do=show" alt="Poster">
          </div>
          {/each}
        {:catch error}
          <p style="display: none;">Error: {error.message}</p>
        {/await}
      </div>
    {/if}
</main>

<style>
:root {
  --blur-rate: 3px;
}
:global(html, body) {
	background-color: black;
	height: 100%;
	-webkit-user-select: none;  
    -moz-user-select: none;    
    -ms-user-select: none;      
    user-select: none;
}
main {
	background-color: black;
    height: 100vh;
}
#grid {
  display: grid;
  grid-gap: 5px;
  background-color: black;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
}
#grid > div {
  font-size: 30px;
  color: #ffffff;
  background-color: black;
  text-align: center;
  border-radius: 20px;
}
#grid > div:hover {
  cursor: pointer;
  animation: blur 0.3s;
  animation-fill-mode: forwards;
}
#grid > div:not(:hover) {
	animation: unblur 0.3s;
	animation-fill-mode: forwards;
}
#grid > div > img {
  height: auto;
  width: 100%;
  background-color: black;
}
input {
  width: 75%;
  height: 7%;
  background-color: #1d1d1d;
  color: white;
  font-size: 2em;
  text-align: center;
  padding-top: 5px;
  padding-bottom: 5px;
  text-decoration: none;
  position: relative;
  border: none;
  margin-bottom: 8vh;
  margin-top: 8vh;
  margin-left: 12.5%;
}
input:focus {
  outline:none !important;
}
@keyframes blur {
  from {
    -webkit-filter: blur(0px);
    -moz-filter: blur(0px);
    -o-filter: blur(0px);
    -ms-filter: blur(0px);
    filter: blur(0px);
  }
  to {
    -webkit-filter: blur(var(--blur-rate));
    -moz-filter: blur(var(--blur-rate));
    -o-filter: blur(var(--blur-rate));
    -ms-filter: blur(var(--blur-rate));
    filter: blur(var(--blur-rate));
  }
}

@keyframes unblur {
    from {
        -webkit-filter: blur(var(--blur-rate));
        -moz-filter: blur(var(--blur-rate));
        -o-filter: blur(var(--blur-rate));
        -ms-filter: blur(var(--blur-rate));
        filter: blur(var(--blur-rate));
    }
    to {
        -webkit-filter: blur(0px);
        -moz-filter: blur(0px);
        -o-filter: blur(0px);
        -ms-filter: blur(0px);
        filter: blur(0px);
    }
}

</style>