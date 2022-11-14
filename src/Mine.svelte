<script>
    import Nav from './Nav.svelte';
	import Featured from './Featured.svelte';
	import axios from 'axios';

    var featuredMetadata = { title: "Loading ...", };
	let showFt = "false";
	let scrollEffect = "false";
    
	const random = (length = 8) => {
		let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
		let str = '';
		for (let i = 0; i < length; i++) {
			str += chars.charAt(Math.floor(Math.random() * chars.length));
		}
		return str;
	};

	const menu = {
		favorites: {
			title: "Favorites",
			url: "/api/favorites/",
			id: random(10)
		},
        playlist: {
			title: "Playlist",
			url: "/api/playlist/",
			id: random(10)
		},
	}
	

    
	// view replace's featured with custom item
	const view = (id) => {
		axios({
			method: 'get',
			url: "/api/getMovieInfo/" + id,
			transformResponse: (res) => {
				return JSON.parse(res);
			},
			responseType: 'json'
		}).then(response => {
			const data = response.data;
			featuredMetadata.img = `/api/poster/${id}?do=show`;
			featuredMetadata.title = data.title;
			featuredMetadata.line = "";
			featuredMetadata.info = data.info;
			featuredMetadata.plot = data.plot;
			featuredMetadata.imdbID = id;
			featuredMetadata.kind = data.kind;
			featuredMetadata.inFavorites = data.inFavorites;
			featuredMetadata.inPlaylist = data.inPlaylist;
            showFt = "true"
			scrollEffect = "true"
			window.scrollTo(0, 0);
		}).catch(error => {
			console.log(error);
		});
	}
</script>

<main>
	<Nav active="mine" scrollEffect="{scrollEffect}"/>
	{#if showFt == "true"}
	<Featured {...featuredMetadata} />
	<br style="font-size: 100px;" />
	{:else}
	<br style="font-size: 50px;" />
	{/if}
	<div id="content" class="content">
			{#each Object.values(menu) as m}
			<h1>{ m.title }</h1>
			<div class="outer">
				{#await axios.get(m.url, {transformResponse: (res) => { return JSON.parse(res).results; }, responseType: 'json'})}
					{ console.log("Getting Movies ...") }
				{:then resp}
					{#each Object.values(resp.data) as d}
						<img on:click={() => view(d.id)} src="/api/poster/{ d.id }?do=show" alt="{ d.title }">
					{/each}
				{:catch error}
					{ console.log("Fuck, Error occured: " + error.message) }
				{/await}
			</div>
			<div class="br"></div>
		{/each}
	</div>
</main>


<style>
	:root {
        --blur-rate: 3px;
    }

	.br {
		width: 100%;
		height: 10vh;
		background-color: black;
		position: relative;
		z-index: 50;
	}

	h1 {
		color: white;
		font-size: 1.5rem;
		margin-left: 5px;
		margin-bottom: 0px!important;
		padding-bottom: 8px!important;
		position: relative;
		z-index: 50;
		background-color: black;
	}
	main {
		background-color: black;
	}
	:global(html, body) {
		background-color: black;
		height: 100%;
		-webkit-user-select: none;  
        -moz-user-select: none;    
        -ms-user-select: none;      
        user-select: none;
	}
	.content > div > img {
		height: 100%;
		margin-left: 5px;
		background-color: black!important;
	}
	.content > div > img:hover {
		cursor: pointer;
		animation: blur 0.3s;
		animation-fill-mode: forwards; 
	}

	.content > div > img:not(:hover) {
		animation: unblur 0.3s;
		animation-fill-mode: forwards;
	}

	.outer {
		width: 100%;
		height: 50vh;
		white-space: nowrap;
		position: relative;
		overflow-x: scroll;
		overflow-y: hidden;
		-webkit-overflow-scrolling: touch;
		background-color: black;
	}

	@media screen and (max-width: 600px) {
        .content {
			margin-left: 5px;
			margin-right: 5px;
		}
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