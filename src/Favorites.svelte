<script>
    import Nav from "./Nav.svelte";
    import axios from "axios";

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
	<Nav active="favorites" scrollEffect="false"/>
    <div class="content">
        {#await axios.get("/api/favorites/", {transformResponse: (res) => { return JSON.parse(res).results; }, responseType: 'json'})}
            <p style="display: none;">Loading ...</p>
        {:then resp}
            <div class="grid-container">
            {#each Object.entries(resp.data) as [i, d]}
                <div class="grid-item card" on:click={()=>{window.location=`/?tab=player&id=${d.id}&kind=${d.kind}`}}>
                    <img src="/api/poster/{ d.id }?do=show" alt="Movie" style="width:100%">
                </div> 
            {:else}
                <h1 style="text-align:center; color: white;">Empty, Please add items to favorites to see them here</h1>
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
    }

    .card:hover {
		cursor: pointer;
		animation: blur 0.3s;
		animation-fill-mode: forwards; 
    }

    img {
        border-radius: 5px 5px 0 0;
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