<script lang="ts">
	import { Range } from 'flowbite-svelte'

	let board_size = 50

	import { Chessground, cgStylesHelper } from 'svelte-use-chessground';
	import 'svelte-use-chessground/cgstyles/chessground.css';

	const pieces = ["r", "n", "b", "q"]
	let  layout = ["k"]
	for (let p=0; p<7; p++) {
		layout.push(pieces[Math.floor(Math.random() * pieces.length)])
	}

	const randomLayout = () => {
		let randomized = layout
		.map(value => ({ value, sort: Math.random() }))
		.sort((a, b) => a.sort - b.sort)
		.map(({ value }) => value)

		return randomized.join("")
	}

	const whiteLineup = randomLayout().toLocaleLowerCase()
	const blackLineup = randomLayout().toUpperCase()

	let fen = whiteLineup+"/pppppppp/8/8/8/8/PPPPPPPP/"+blackLineup+" w KQkq - 0 1"
	let move_color="white"
	let legal= new Map([
          ['h2', ['h4']]
        ])

	let cgApi;
	let config = {
		movable:{
			free:false,
			color:move_color,
			dests:legal,
		},
		premovable:{
			enabled:false,
		},
		fen:fen,
	};

	function initializer(api: any) {
		cgApi = api;
		// A named function might not be necessary but I've encountered infinite loops while using an inline initializer function.
	}

</script>

<div class="xl:grid grid-cols-3">
	<div class="col-span-2 flex justify-center items-center">
		<div
			style="width:{board_size}%;aspect-ratio:1"
			use:Chessground={{config, initializer}}
			use:cgStylesHelper="{{ piecesFolderUrl: 'game/pieces/', boardUrl: 'game/board_blue.svg' }}"
		/>
	</div>	

	<div class="">
		<div class="m-3">
			Adjust Board Size
			<Range id="range1" min={25} max={95} bind:value={board_size}/>
		</div>
		<div class="m-3">
			Board Theme
			(TODO)
		</div>
		<div class="m-3">
			Piece Set
			(TODO)
		</div>
	</div>
</div>