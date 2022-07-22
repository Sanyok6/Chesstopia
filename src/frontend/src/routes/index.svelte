<script>
	import { Button } from 'flowbite-svelte';

    const words = ["amazing", "cool", "insane", "awesome"];

    let index = 0;

    const handleClick = () => {
        index = words.length % index+1       
    };

</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<Button on:click="{handleClick}">This is {words[index]}!</Button>
