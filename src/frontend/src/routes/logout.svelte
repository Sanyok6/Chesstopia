<script type="ts">
    import { fetchApi } from "$lib/api";
    import { userStore, type User } from "$lib/store";
    import { onMount } from "svelte";

    onMount(() => {
        fetchApi("auth/logout/", {method:"POST"}).then(() => {
            userStore.set(null);
        });
    })

</script>

<div class="text-center">
    <p>Logout sucsessful!</p>
    <a class="text-blue-500 underline" href="/welcome" >Return to welcome page</a>
</div>