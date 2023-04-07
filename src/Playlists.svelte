<script>
    import Nav from "./Nav.svelte";
    import axios from "axios";

    var showOptions = false;
    let addons = [];
    axios({
	    method: 'get',
		url: "/api/addons",
		transformResponse: (res) => { return JSON.parse(res); },
		responseType: 'json'
	}).then(response => {
		const data = response.data;
        data.forEach(element => {
            if (element.open) {
                addons.push(element);
            }
        });
	}).catch(error => {
		console.log(error);
	});
</script>

<main>
	<Nav active="playlists" scrollEffect="false"/>
    <div class="content">
        {#await axios.get("/api/playlists", {transformResponse: (res) => { return JSON.parse(res).results; }, responseType: 'json'})}
            <p style="display: none;">Loading ...</p>
        {:then resp}
            <div class="grid-container">
            {#each Object.entries(resp.data) as [i, d]}
                <div class="grid-item card" id="{i}">
                    <button 
                    on:mouseover={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:focus={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:mouseout={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:blur={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:click={()=>{
                        showOptions = !showOptions;
                    }}
                    >Options {showOptions ? '▲' : '▼'}</button>


                    {#if showOptions}
                    <!-- svelte-ignore missing-declaration -->
                    <button 
                    on:mouseover={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:focus={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:mouseout={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:blur={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:click={()=>{
                        let newImage = prompt("Enter image URL:", "");
                        if (newImage == null || newImage == "") { return; }

                        let xhr = new XMLHttpRequest();
                        xhr.open("GET", `/api/changeIcon?image=${newImage}&playlistID=${d.playlistID}`, true);
                        xhr.onreadystatechange = function() {
                        if (xhr.readyState == 4 && xhr.status == 200) { 
                                window.location.reload();
                            }
                        };
                        xhr.send();
                    }}
                    >Change Icon</button>

                    <button 
                    on:mouseover={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:focus={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:mouseout={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:blur={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:click={(e)=>{
                        navigator.clipboard.writeText(`${window.location.origin}?tab=playlist&id=${d.playlistID}`);
                        e.originalTarget.innerText = "Copied";

                        window.setTimeout(function(){
                            e.originalTarget.innerText = "Share";
                        }, 1000);
                    }}
                    >Share</button>

                    <!-- svelte-ignore missing-declaration -->
                    <button 
                    on:mouseover={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:focus={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:mouseout={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:blur={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    on:click={()=>{
                        let newTitle = prompt("Change title:", "");
                        if (newTitle == null || newTitle == "") { return; }

                        let xhr = new XMLHttpRequest();
                        xhr.open("GET", `/api/renamePlaylist?title=${newTitle}&playlistID=${d.playlistID}`, true);
                        xhr.onreadystatechange = function() {
                        if (xhr.readyState == 4 && xhr.status == 200) { 
                                window.location.reload();
                            }
                        };
                        xhr.send();
                    }}
                    >Rename</button>

                    <!-- svelte-ignore missing-declaration -->
                    <button 
                        on:mouseover={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                        on:focus={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                        on:mouseout={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                        on:blur={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                        on:click={()=>{
                            let xhr = new XMLHttpRequest();
                            xhr.open("GET", `/api/deletePlaylist/${d.playlistID}`, true);
                            xhr.onreadystatechange = function() {
                            if (xhr.readyState == 4 && xhr.status == 200) { 
                                    window.location.reload();
                                }
                            };
                            xhr.send();
                        }}
                    >Delete</button>
                    {/if}
                    <div
                        on:click={()=>{window.location=`/?tab=playlist&id=${d.playlistID}`}}
                        on:mouseover={()=>{document.getElementById(i.toString()).style.borderColor='beige'}}
                        on:focus={()=>{document.getElementById(i.toString()).style.borderColor='beige'}}
                        on:mouseout={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                        on:blur={()=>{document.getElementById(i.toString()).style.borderColor='blue'}}
                    >
                        <img src="https://corsproxy.io/?{encodeURIComponent(d.logo)}" alt="Playlist" style="width:100%">
                        <div class="container">
                            <h4><b>{ d.title }</b></h4>
                        </div>
                    </div>
                </div> 
            {/each}
            </div>
        {:catch error}
            <p style="display: none;">Error: {error.message}</p>
        {/await}
    </div>
</main>


<style>
    main {
        background-color: black;
        height: 100%;
    }

    .card h4 {
        text-align: center;
        color: white;
    }

    .card button {
        border-radius: 5px;
        background-color: black;
        border: 3px solid blue;
        color: beige;
    }

    .card button:hover {
        border: 3px solid red;
    }

    .container {
        padding: 2px 16px;
    }

    .grid-container {
        display: grid;
        grid-template-columns: auto auto auto auto auto auto auto;
        position: absolute;
        left: 50%;
        transform: translate(-50%);
        width: 90vw;
        gap: 10px;
        margin-top: 100px;
    }

    .grid-item {
        font-size: 30px;
        text-align: center;
    }

    .card {
        max-width: 280px;
        min-width: 40%;
        border-radius: 5px;
        background-color: black;
        border: 2px solid blue;
    }

    .card:hover {
		cursor: pointer;
    }

    img {
        border-radius: 5px 5px 0 0;
    }
</style>