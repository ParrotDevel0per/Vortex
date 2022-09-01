<script>
    import Home from './Home.svelte';
    import Mine from './Mine.svelte';
</script>


{#if tab == "search"}
{ console.log("search") }
{:else if tab == "mine"}
<Mine />
{:else}
<Home id="{ id }" showG="{ showG }" kind="{ kind }" showFt = "{ showFt }"/>
{/if}