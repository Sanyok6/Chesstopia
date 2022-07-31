<script>
	import { Button } from 'flowbite-svelte';

    const game_mode_description_style = `w-1/3 rounded-lg group text-center font-medium focus:outline-none p-0.5
             text-white bg-gradient-to-br from-purple-600 to-blue-500 focus:ring-blue-300
             dark:focus:ring-blue-800 mb-7 mx-5`;
</script>

<div class="flex h-1/2 justify-center items-center">
	<div class="text-center">
		<h1 class="font-extralight text-6xl dark:text-white my-36">Welcome to Chesstopia!</h1>
		<div class="flex justify-center text-center mb-10">
			<div class={game_mode_description_style}>
                <h1 class="text-3xl">Confusion Chess</h1>
                <p class="m-2">Confusion chess is a game mode which allows a players piece layout to
                    be different than the standard chess layout, with a different amount of pieces.
					This may seem like a bug... But wait... This is actually a feature! Confusion Chess
					allows players to focus on thier positional thinking since standard openings dont work here! </p>
			</div>
			<div class={game_mode_description_style}>
                <h1 class="text-3xl">Magic Chess</h1>
                <p class="m-2">Magic chess is a game mode which allows players to bypass move
                   validation for some pieces. While this may seem like a bug, it allows for some 
				   supper fun, and crazy chess games! 
                </p>
			</div>
		</div>
		<a href="/login" class="mt-20">
			<Button outline gradient color="purpleToBlue" shadow="blue" size="lg">
				Enter Chesstopia
			</Button>
		</a>
	</div>
</div>
