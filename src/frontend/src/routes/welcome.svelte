<script>
	import { Button } from 'flowbite-svelte';
</script>

<main>
	<div>
		<h1>Welcome to Chesstopia!</h1>
		<br />
		<a href="/">
			<Button href="/dashboard" outline gradient color="purpleToBlue" shadow="blue">
				Enter Chesstopia
			</Button>
		</a>
	</div>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		font-size: 4em;
		font-weight: 40;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>