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
                <p class="m-2">Confusion chess is a game mode which allows players piece layout to
                    be different than the standard chess piece layout. This pushes the players skill
                    because they won't know the piece layout and what pieces they'll get until the game starts.
                    Hence standard openings won't work in this game mode</p>
			</div>
			<div class={game_mode_description_style}>
                <h1 class="text-3xl">Magic Chess</h1>
                <p class="m-2">Magic chess is a game mode which allows players to by pass move
                   validation sometimes. Players can take this to their advantage by making moves that are
                   not valid in the standard chess
                </p>
			</div>
		</div>
		<a href="/login">
			<Button outline gradient color="purpleToBlue" shadow="blue">
				Enter Chesstopia
			</Button>
		</a>
	</div>
</div>
