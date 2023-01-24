<script>
	import Nav from './Nav.svelte';
	import axios from 'axios';
    
    let rerender = false;

    let defaultC = [];
    axios({
		method: 'get',
		url: "/api/defaultHome",
		responseType: 'json',
        transformResponse: (res) => { return JSON.parse(res); }
	}).then(response => {
		defaultC = response.data;
	}).catch(error => {
		console.log(error);
	});

    let categories = [];
    axios({
		method: 'get',
		url: "/api/userInfo",
		responseType: 'json',
        transformResponse: (res) => { return JSON.parse(res); }
	}).then(response => {
		categories = response.data["home"];
	}).catch(error => {
		console.log(error);
	});

    const handleClick = (title) => {
        for (var i=0; i<categories.length; i++)  {
            if (categories[i]["title"] == title) {
                if (categories[i]["enabled"] == true) categories[i]["enabled"] = false
                else if (categories[i]["enabled"] == false) categories[i]["enabled"] = true
                break;
            }
        }
        rerender = !rerender;
    }

    $: {
        if (categories != [] && categories != undefined) {
            axios({
                method: 'get',
                url: "/api/updateHomeMenu?new=" + btoa(JSON.stringify(categories)),
                responseType: 'json'
            }).then(response => {
                console.log(response.data);
            }).catch(error => {
                console.log(error);
            });  
        }
    }

    const openclose = (id, o="block") => {
        const item = document.getElementById(id);
        if (item.style.display == "none") {
            item.style.display = o
        } else {
            item.style.display = "none"
        }
    }
</script>

<main>
	<Nav active="home" scrollEffect="false"/>
    <br style="font-size: 100px;" />
    <div class="content">
        <button on:click={()=>{openclose("homeSettings", "flex")}}>Home Settings</button>
        <div id="homeSettings" style="display: none;">
        {#key rerender}
            {#each categories as category}
                {#if category["title"] != "Playlist"}
                    <button 
                        class="{category["enabled"] ? 'enabled' : 'disabled'}"
                        on:click={()=>{handleClick(category["title"])}}
                    >{ category["title"] }</button>
                {/if}
            {/each}
        {/key}
        <button class="default" style="color: blue;" on:click={()=>{categories=defaultC}}>Defaults</button>
        </div>
    </div>
</main>


<style>
	:global(html) {
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
        width: 100vw;
	}
    .content {
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items:center;
        width: 100vw;
    }

    #homeSettings {
        width: 100%;
        justify-content: center;
        align-items: center;
        display: flex;
        flex-direction: column;
        padding: 30px;
        padding-top: 0px;
    }
    
    .enabled {
        border: 2px solid blue;
    }
    

    button {
        width: 50%;
        display: block;
        height: 6vh;
        background-color: black;
        border: 3px solid black;
        color: white;
    }
    button:hover {
        border: 3px solid white;
    }

</style>