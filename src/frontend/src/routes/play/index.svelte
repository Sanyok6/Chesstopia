<script lang="ts">
	import { Range } from 'flowbite-svelte'

	let board_size = 50

	import { Chessground, cgStylesHelper } from 'svelte-use-chessground';
	import 'svelte-use-chessground/cgstyles/chessground.css';

	let cgApi;
	let config = {height: '400px'};

	function initializer(api: any) {
		cgApi = api;
		// A named function might not be necessary but I've encountered infinite loops while using an inline initializer function.
	}

</script>

<div class="xl:grid grid-cols-3">
	<div class="col-span-2 flex justify-center items-center">
		<div
			style="width:{board_size}%;aspect-ratio:1"
			use:Chessground="{{config, initializer}}"
			use:cgStylesHelper="{{ piecesFolderUrl: 'game/pieces/', boardUrl: 'game/board_blue.svg' }}"
		/>
	</div>	

	<div class="">
		<div class="m-3">
			Adjust Board Size
			<Range id="range1" min=25 max=95 bind:value={board_size}/>
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