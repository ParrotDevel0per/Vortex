<script>
	import Nav from './Nav.svelte';
	import Featured from './Featured.svelte';
	import axios from 'axios';
	import 'boxicons'

	// Grab url parameters
	const params = new URLSearchParams(window.location.search);
    const showG = params.get("showG") ? params.get("showG") : "true";
	const showFt = params.get("showFt") ? params.get("showFt") : "true";
	const id = params.get("id") ? params.get("id") : "";

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
		preloadImage(`/api/banner/${id}?do=show`);
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
			window.scrollTo(0, 0);
			if (item) item.src = before;
		}).catch(error => {
			console.log(error);
		});
	}
	if (id) {view(id)}

	const scrollRight = (id) => {
		let item = document.getElementById(id);
		item.scrollLeft = item.scrollLeft + 500
	}
	const scrollLeft = (id) => {
		let item = document.getElementById(id);
		item.scrollLeft = item.scrollLeft - 500
	}
</script>

<main>
	<Nav active="home"/>
	{#if showFt == "true"}
	<Featured {...featuredMetadata} />
	{/if}
	<div id="content" class="content">
		<!--<br style="font-size: 100px;" />-->
		{#if showG == "true"}
			{#each homeItem as m}
				{#if m.enabled == true}
					{#await axios.get(m.url, {transformResponse: (res) => { return JSON.parse(res).results; }, responseType: 'json'})}
						<p style="display: none;">Loading ...</p>
					{:then resp}
					<!--<h1>{ m.title }</h1>-->
					<div on:click={()=>{scrollLeft(`${m.title}Box`)}} class="arrows left">
						<box-icon name='chevron-left' color="white"></box-icon>
					</div>
					<div on:click={()=>{scrollRight(`${m.title}Box`)}} class="arrows right">
						<box-icon name='chevron-right' color="white"></box-icon>
					</div>
					<div id="{m.title}Box" class="outer">
						<div class="placeholder"></div>
						{#each Object.values(resp.data) as d}
							<img class="clickablePoster" on:click={() => view(d.id)} id={d.id} src="/api/poster/{ d.id }?do=show" alt="{ d.title }">
						{/each}
						<!--<div class="br"></div>-->
					</div>
					{:catch error}
						<p style="display: none;">Error: {error.message}</p>
					{/await}
				{/if}
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

	main {
		background-color: black;
	}

	box-icon {
		width: 100%!important;
		height: 100%!important;
	}

	.placeholder {
		width: 50px;
		height: 48.2vh;
	}

	.arrows {
		position: absolute;
		width: 50px;
		height: 50vh;
		background-color: #101214;
		z-index: 999;
	}

	.left {
		left: 0;
	}
	
	.right {
		right: 0;
	}

	.content {
		box-sizing: border-box;
		background-color: black;
		z-index: 10;
		position: relative;
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
		margin-bottom: 2%;
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