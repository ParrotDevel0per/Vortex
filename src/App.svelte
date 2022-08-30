<script>
	import Nav from './Nav.svelte';
	import Featured from './Featured.svelte';
	import axios from 'axios';
	
	
	const random = (length = 8) => {
		let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
		let str = '';
		for (let i = 0; i < length; i++) {
			str += chars.charAt(Math.floor(Math.random() * chars.length));
		}
		return str;
	};

	const menu = {
		bestActionMovies: {
			title: "Action",
			url: "/api/getMoviesByGenres?genres=Action",
			id: random(10)
		},
		bestWarMovies: {
			title: "War",
			url: "/api/getMoviesByGenres?genres=War",
			id: random(10)
		},
		bestComedyMovies: {
			title: "Comedy",
			url: "/api/getMoviesByGenres?genres=Comedy",
			id: random(10)
		},
		bestAnimatedMovies: {
			title: "Animated",
			url: "/api/getMoviesByGenres?genres=Animation",
			id: random(10)
		},
	}

	var featuredMetadata = {
        img: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.wallpapersden.com%2Fimage%2Fdownload%2Fjoker-2019-movie-poster_66602_2560x1440.jpg&f=1&nofb=1",
        title: "JOKER",
        line: "SMILE AND PUT ON A HAPPY FACE",
        info: "8.4/10\u00A0\u00A02019\u00A0\u00A0Crime, Drama, Thriller\u00A0\u00A02h 20m",
        plot: "A socially inept clown for hire - Arthur Fleck aspires to be a stand up comedian among his small job working dressed as a clown holding a sign for advertising. He takes care of his mother- Penny Fleck, and as he learns more about his mental illness, he learns more about his past. Dealing with all the negativity and bullying from society he heads downwards on a spiral, in turn showing how his alter ego \"Joker\", came to be.",
		id: ""
    };
	

	const view = (id, type) => {
		let modal = document.getElementById("infoModal");
		let content = document.getElementById("content");
		axios({
			method: 'get',
			url: "/api/getMovieInfo/" + id,
			transformResponse: (res) => {
				return JSON.parse(res);
			},
			responseType: 'json'
		}).then(response => {
			content.style.display = "none";
			modal.style.display = "block";
		}).catch(error => {
			console.log(error);
		});
	}
</script>

<main>
	<Nav />
	<div id="content" class="content">
		<Featured 
			img = "{ featuredMetadata.img }"
			title = "{ featuredMetadata.title }"
			line = "{ featuredMetadata.line }"
			info = "{ featuredMetadata.info }"
			plot = "{ featuredMetadata.plot }"
			id = "{ featuredMetadata.id }"
		/>
		<br style="font-size: 100px;" />
		{#each Object.values(menu) as m}
			<h1>{ m.title }</h1>
			<div class="outer">
				{#await axios.get(m.url, {transformResponse: (res) => { return JSON.parse(res).results; }, responseType: 'json'})}
					{ console.log("Getting Movies ...") }
				{:then resp}
					{#each Object.values(resp.data) as d}
						<img on:click={() => view(d.id, d.kind)} src="/api/poster/{ d.id }?do=show" alt="{ d.title }">
					{/each}
				{:catch error}
					{ console.log("Fuck, Error occured: " + error.message) }
				{/await}
			</div>
		{/each}
	</div>
	<div class="infoModal" id="infoModal">
		<img src="/api/poster/tt3152592?do=show" alt="">
	</div>
</main>


<style>
	:root {
        --blur-rate: 3px;
    }

	h1 {
		color: #bdc3ca;
		font-size: 1.5rem;
		margin-left: 5px;
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
	}
	.content > div > img:hover {
		cursor: pointer;
		animation: blur 0.3s;
		animation-fill-mode: forwards; 
	}
	.outer {
		width: 98%;
		height: 50vh;
		white-space: nowrap;
		position: relative;
		overflow-x: scroll;
		overflow-y: hidden;
		-webkit-overflow-scrolling: touch;
		margin-bottom: 10vh;
	}

	@media screen and (max-width: 600px) {
        .content {
			margin-left: 5px;
			margin-right: 5px;
		}
    }

	.infoModal {
		display: none;
		height: 90vh;
		width: 100vw;
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

</style>