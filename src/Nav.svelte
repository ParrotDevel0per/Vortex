<script>
  export let active;
  export let scrollEffect = "true";
  var nav = "";

  window.addEventListener('scroll', () => {
    if (scrollEffect == "false") { nav.style.backgroundColor = `black`; return; }
    let y = 1 + (window.scrollY || window.pageYOffset) / 150
    y = y < 1 ? 1 : y // ensure y is always >= 1 (due to Safari's elastic scroll)
    //console.log(y); // for debugging
    if (y < 5.76) {
      nav.style.backgroundColor = `transparent`;
    } else {
      nav.style.backgroundColor = `black`;
    }
  })

  $: {
    try {
      if (scrollEffect == "false") { nav.style.backgroundColor = `black`; }
      else { nav.style.backgroundColor = `transparent`; }
    }
    catch {
      console.log("Nav not yet created, :pepesad:")
    }
  }
</script>

<nav bind:this={nav} class="navbar navbar-expand-lg fixed-top">
    <a class="navbar-brand" href="/">The Pirate Player</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          {#if active == "home"}
          <a class="nav-link active" href="/">Home</a>
          {:else}
          <a class="nav-link" href="/">Home</a>
          {/if}
        </li>
        <li class="nav-item">
          {#if active == "search"}
          <a class="nav-link active" href="/?tab=search">Search</a>
          {:else}
          <a class="nav-link" href="/?tab=search">Search</a>
          {/if}
        </li>
        <li class="nav-item">
          {#if active == "mine"}
          <a class="nav-link active" href="/?tab=mine">Mine</a>
          {:else}
          <a class="nav-link" href="/?tab=mine">Mine</a>
          {/if}
        </li>
      </ul>
    </div>
</nav>


<style>
@font-face {
  font-family: 'Chomsky';
  src: url('/static/fonts/Chomsky.woff') format('woff');
}

/*
.custom {
  margin-left: 67%!important;
  width: 20%!important;
  background-color: black!important;
  border: 0px;
  border-bottom: #6d737a 3px solid;
}
*/

nav {
  background-color: transparent;
  width: 100%;
  margin-bottom: 10px;
}

.navbar-brand {
  font-family: 'Chomsky';
  color: rgb(255, 0, 0)!important;
  margin-right: 2%!important;
  padding-left: 1%;
}

.nav-link {
  color:  #3d3d3d!important;
}

.active {
  color: #6d737a!important;
}
</style>