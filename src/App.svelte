<script>
    import Home from './Home.svelte';
    import Mine from './Mine.svelte';
    import Search from './Search.svelte';
</script>


{#if tab == "search"}
<Search />
{:else if tab == "mine"}
<Mine />
{:else}
<Home id="{ id }" showG="{ showG }" showFt = "{ showFt }"/>
{/if}