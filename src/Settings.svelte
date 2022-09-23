<script>
	import Nav from './Nav.svelte';
	import axios from 'axios';
    let data = "";
    let textarea = "";
    axios({
		method: 'get',
		url: "/api/homeMenu",
        transformResponse: (res) => { return res; },
		responseType: 'json'
	}).then(response => {
		data = response.data
	}).catch(error => {
		console.log(error);
	});

    const handleClick = () => {
        axios({
            method: 'get',
            url: "/api/updateHomeMenu?new=" + btoa(textarea.value),
            responseType: 'text'
        }).then(response => {
            return
        }).catch(error => {
            console.log(error);
        });

    }

</script>

<main>
	<Nav active="home" scrollEffect="false"/>
    <br style="font-size: 100px;" />
    <div class="content">
        <textarea bind:this={textarea} name="Home" rows="4" cols="50">{ data }</textarea>
        <button on:click={() => {handleClick()}}>Update</button>
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
    textarea {
        width: 50%;
        background-color: black;
        color: white;
        resize: both;
        height: 70vh;
    }
    textarea:focus {
        outline: none!important;
    }
    button {
        width: 50%;
        height: 6vh;
        background-color: black;
        border: 3px solid black;
        border-top: 0px !important;
        color: white;
    }
    button:hover {
        border: 3px solid white;
    }

</style>