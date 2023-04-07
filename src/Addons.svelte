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
	<Nav active="addons" scrollEffect="false"/>
    <div class="content">
        {#await axios.get("/api/addons", {transformResponse: (res) => { return JSON.parse(res); }, responseType: 'json'})}
            <p style="display: none;">Loading ...</p>
        {:then resp}
            <div class="grid-container">
            {#each Object.entries(resp.data) as [i, d]}
                <div class="grid-item card" on:click={()=>{window.location=d.open ? d.open : "#"}}>
                    <img src="/api/addonLogo/{ d.id }" alt="Addon" style="width:100%">
                    <div class="container">
                    <h4><b>{ d.name }</b></h4>
                    </div>
                </div> 
            {:else}
                <h1 style="text-align:center; color: white;">Empty, Please install some addons to see them here</h1>
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
        overflow-y: hidden;
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
        border-color: beige;
    }

    .card h4 {
        text-align: center;
        color: white;
    }

    img {
        border-radius: 5px 5px 0 0;
    }

    .container {
        padding: 2px 16px;
    }
</style>