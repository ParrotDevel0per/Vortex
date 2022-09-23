<script>
    import Home from './Home.svelte';
    import Mine from './Mine.svelte';
    import Search from './Search.svelte';
    import Settings from './Settings.svelte';
</script>


{#if tab == "search"}
<Search />
{:else if tab == "mine"}
<Mine />
{:else if tab == "settings"}
<Settings />
{:else}
<Home id="{ id }" showG="{ showG }" showFt = "{ showFt }"/>
{/if}