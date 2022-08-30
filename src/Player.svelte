<script>
    export let imdbID = "";

    var player = new Playerjs({
        id:"player",
        file:"{{ resolved }}",
        poster:"/static/img/preloader/1.png",
    });
</script>

<main>
    <div id="player"></div>
</main>

<style>

</style>