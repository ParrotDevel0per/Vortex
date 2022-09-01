<script>
    import Home from './Home.svelte';
    import Favorites from './Favorites.svelte';
    import Playlist from './Playlist.svelte';
</script>


{#if tab == "favs"}
<Favorites />
{:else if tab == "playlist"}
<Playlist />
{:else}
<Home id="{ id }" showG="{ showG }" kind="{ kind }" showFt = "{ showFt }"/>
{/if}

<style>

</style>