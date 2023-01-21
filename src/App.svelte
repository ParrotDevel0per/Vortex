<script>
    import Home from './Home.svelte';
    import Favorites from './Favorites.svelte';
    import Search from './Search.svelte';
    import Settings from './Settings.svelte';
    import Addons from './Addons.svelte';
    import Playlists from './Playlists.svelte';
    import Playlist from './Playlist.svelte';
</script>


{#if tab == "search"}
<Search />
{:else if tab == "favorites"}
<Favorites />
{:else if tab == "playlists"}
<Playlists />
{:else if tab == "playlist"}
<Playlist />
{:else if tab == "addons"}
<Addons />
{:else if tab == "settings"}
<Settings />
{:else}
<Home id="{ id }" showG="{ showG }" showFt = "{ showFt }"/>
{/if}

<style>
:global(html)::-webkit-scrollbar {
  display: none;
}


:global(html) {
  -ms-overflow-style: none;  
  scrollbar-width: none;  
} 
</style>