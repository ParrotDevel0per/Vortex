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
</script>

<main>
	<Nav active="home" scrollEffect="false"/>
    <br style="font-size: 100px;" />
    <div class="content">
        {#key rerender}
            {#each categories as category}
                <button 
                    class="{category["enabled"] ? 'enabled' : 'disabled'}"
                    on:click={()=>{handleClick(category["title"])}}
                >{ category["title"] }</button>
            {/each}
        {/key}
        <button class="default" on:click={()=>{categories=defaultC}}>Defaults</button>
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
    
    .enabled {
        border: 3px solid green;
    }
    
    .disabled {
        border: 3px solid red;
    }
    button {
        width: 50%;
        height: 6vh;
        background-color: black;
        border: 3px solid black;
        color: white;
    }
    button:hover {
        border: 3px solid white;
    }

</style>