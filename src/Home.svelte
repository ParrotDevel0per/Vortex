<script>
	import Nav from './Nav.svelte';
	import Featured from './Featured.svelte';
	import axios from 'axios';
	export let showG;
	export let id;
	export let showFt;

	var homeItem = [];
	if (showG == "true") {
		axios({
			method: 'get',
			url: "/api/homeMenu",
			transformResponse: (res) => { return JSON.parse(res); },
			responseType: 'json'
		}).then(response => {
			const data = response.data;
			homeItem = data;
			window.scrollTo(0, 0);
		}).catch(error => {
			console.log(error);
		});
	}

	var featuredMetadata = { title: "Loading ...", };
	// if id ain't  defined get featured from api
	if (!id) {
		axios({
			method: 'get',
			url: "/api/featured",
			transformResponse: (res) => {
				return JSON.parse(res);
			},
			responseType: 'json'
		}).then(response => {
			const data = response.data;
			featuredMetadata = {
				img: data.img,
				title: data.title,
				line: data.line,
				info: data.info,
				plot: data.plot,
				imdbID: data.imdbID,
				kind: data.kind,
				inPlaylist: data.inPlaylist,
				inFavorites: data.inFavorites,
				episodeCount: data.episodeCount
			}
			window.scrollTo(0, 0);
		}).catch(error => {
			console.log(error);
		});
	}

	function preloadImage(url) {
		var img=new Image();
		img.src=url;
	}
	preloadImage("/static/img/loading.gif")

	// view replace's featured with custom item
	const view = (id) => {
		let item = document.getElementById(id);
		let before = "";

		if (item) {
			before = item.src;
			item.src = "/static/img/loading.gif";
		}
		
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
			featuredMetadata.NOS = data.NOS;
			featuredMetadata.episodeCount = data.episodeCount;
			window.scrollTo(0, 0);
			if (item) item.src = before;
		}).catch(error => {
			console.log(error);
		});
	}
	if (id) {view(id)}
</script>

<main>
	<Nav active="home"/>
	{#if showFt == "true"}
	<Featured {...featuredMetadata} />
	{/if}
	<div id="content" class="content">
		<br style="font-size: 100px;" />
		{#if showG == "true"}
			{#each homeItem as m}
				{#await axios.get(m.url, {transformResponse: (res) => { return JSON.parse(res).results; }, responseType: 'json'})}
					<p style="display: none;">Loading ...</p>
				{:then resp}
				<h1>{ m.title }</h1>
				<div class="outer">
					{#each Object.values(resp.data) as d}
						<img on:click={() => view(d.id)} id={d.id} src="/api/poster/{ d.id }?do=show" alt="{ d.title }">
					{/each}
					<div class="br"></div>
				</div>
				{:catch error}
					<p style="display: none;">Error: {error.message}</p>
				{/await}
			{/each}
		{/if}
	</div>
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