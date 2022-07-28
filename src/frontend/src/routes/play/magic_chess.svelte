<script>
	import { Chess } from 'chess.ts';

	const EMPTYBOARDFEN = '8/8/8/8/8/8/8/8 w - - 0 1';

	/**
	 * @param {string | undefined} [square]
	 * @param {string | undefined} [FEN]
	 * @param {string | undefined} [pieceType]
	 * @param {string | undefined} [pieceColor]
	 */
	function magicChessMoves(pieceType, pieceColor, square, FEN) {
		// Creates a new instance of chess game to calculate moves
		const chess = new Chess(EMPTYBOARDFEN);
		chess.put({ type: pieceType, color: pieceColor }, 'h1');
		chess.moves();
		const moves = chess.moves({ square: square });
		// by default first char is the piece type, last char is # if the move causes checkmate
		// stripping both for now.
		return moves.map(move => (move.slice(1)).replace('#', ""));
	}

	const pieceType = 'q';
	const pieceColor = 'w';
	const square = 'h1';
	const FEN = EMPTYBOARDFEN;

	const magicMoves = magicChessMoves(pieceType, pieceColor, square, FEN);
	console.log(magicMoves);

</script>

<div class="flex h-1/2 justify-center items-center">
	<div class="text-center">
		<h1 class="font-extralight text-6xl dark:text-white my-36">
			Chess is happening in the background!
		</h1>
		<a href="/" />
	</div>
</div>
