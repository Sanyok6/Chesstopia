<script lang="ts">
	import { Chessground, cgStylesHelper } from 'svelte-use-chessground';
	import 'svelte-use-chessground/cgstyles/chessground.css';

	let cgApi;
	let config = {};

	function initializer(api: any) {
		cgApi = api;
		// A named function might not be necessary but I've encountered infinite loops while using an inline initializer function.
	}
</script>

<div
	use:Chessground="{{config, initializer}}"
	use:cgStylesHelper="{{ piecesFolderUrl: '/images/pieces/merida', boardUrl: '/images/board/blue.svg' }}"
/>