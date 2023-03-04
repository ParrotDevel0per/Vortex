<script>
    import Nav from './Nav.svelte';
	import axios from 'axios';
    import { each } from 'svelte/internal';
	let source;
	let season;
	let episode;
	let player;
	let rerender = true;
	
	// Grab url parameters
	const params = new URLSearchParams(window.location.search);
	const id = params.get("id") ? params.get("id") : "";
	const kind = params.get("kind") ? params.get("kind") : "movie";

	let sources = [];
	
	
	axios({
			method: 'get',
			url: `/api/sources/${id}?kind=${kind}`,
			transformResponse: (res) => { return JSON.parse(res); },
			responseType: 'json'
		}).then(response => {
			sources = response.data;
		}).catch(error => {
			console.log(error);
		});



	const changeSource = (force=false) => {
		rerender = !rerender;
		if (kind == "show") {
			if (
				source == player.dataset.source &&
				season == player.dataset.season &&
				episode == player.dataset.episode &&
				force == false
			) return;

			player.dataset.source = source;
			player.dataset.season = season;
			player.dataset.episode = episode;
			player.src = document.querySelector(`#selectEpisode option[value=${episode}]`).dataset.url;
			rerender = !rerender;
			return
		}


		if (source == player.dataset.source && force==false) return;

		player.dataset.source = source
		player.src = document.querySelector(`#selectSource option[value=${source}]`).dataset.url;
		rerender = !rerender;
	}
</script>

<main>
	<Nav/>
	<div id="content" class="content">
		{#key rerender}
			<select name="Source" id="selectSource" bind:value={source} on:change={()=>changeSource()}>
				{#each sources as s}
				<option value={s.id} data-url={s.url}>{s.name}</option>
				{/each}
			</select>

			{#if kind == "show"}
			<select name="Season" id="selectSeason" bind:value={season} on:change={()=>{changeSource()}}>
				{#each sources as s}
					{#each s.seasons as ss}
						{#if s.id == source}
						<option value={ss.id}>{ss.name}</option>
						{/if}
					{/each}
				{/each}
			</select>



			<select name="Episode" id="selectEpisode" bind:value={episode} on:change={()=>changeSource()}>
				{#each sources as s}
					{#each s.seasons as ss}
						{#if ss.id == season && s.id == source}
							{#each ss.episodes as sse}
							<option value={sse.id} data-url={sse.url}>{sse.name}</option>
							{/each}
						{/if}
					{/each}
				{/each}
			</select>

			{/if}
		{/key}
		<button on:click={()=>changeSource(true)}>Reload</button>

		<div class="p">
			<iframe
				title="Iframe Player"
				id="player"
				data-source=""
				data-season=""
				data-episode=""
				src="about:blank"
				frameborder="0"
				bind:this={player}
				on:load={()=>changeSource()}>
			</iframe>
		</div>
	</div>
</main>


<style>
	:root {
        --blur-rate: 3px;
    }
	:global(html),
	:global(body) {
		background-color: black;
		height: 100%;
		-webkit-user-select: none;  
        -moz-user-select: none;    
        -ms-user-select: none;      
        user-select: none;
	}

	select {
		margin-top: 100px;
		border: 1px solid blue;
		background-color: black;
		font-size: 1rem;
		color: white;
		margin-left: 17px;
	}

	button {
		margin-top: 100px;
		border: 1px solid blue;
		background-color: black;
		font-size: 1rem;
		color: white;
		margin-left: 17px;
	}

	main {
		background-color: black;
		height: 100vh;
		overflow-y: hidden;
	}

	iframe {
		width: 98vw;
		left: 50%;
		position: absolute;
		transform: translate(-50%);
		height: 81vh;
	}

	.content {
		box-sizing: border-box;
		background-color: black;
		z-index: 10;
		position: relative;
	}


	@media screen and (max-width: 600px) {
        .content {
			margin-left: 5px;
			margin-right: 5px;
		}
    }
</style>