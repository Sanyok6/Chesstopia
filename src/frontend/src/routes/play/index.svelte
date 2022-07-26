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
	let legal= new Map([])

	let cgApi;

	let config = {
		movable:{
			free:false,
			dests:legal,
			events: {after: play}
		},
		premovable:{
			enabled:false,
		},
		fen:fen,
	};

	const updateConfig = () => {
		config.movable.dests = legal
		config.fen = fen
	}


	function initializer(api: any) {
		cgApi = api;
		// A named function might not be necessary but I've encountered infinite loops while using an inline initializer function.
	}

	import { Chess } from 'chess.ts'
	const chess = new Chess()

	function play(from: string, to: string) {
		chess.move({ from: from, to: to })
		if (!chess.gameOver()) {
			const moves = chess.moves()
			const move = moves[Math.floor(Math.random() * moves.length)]
			chess.move(move)
			fen=chess.fen()

			generateLegalMoves()
			
			updateConfig()
			//setTimeout(play, 10)
		}
	}

	function generateLegalMoves() {
		const nowLegal = chess.moves({verbose:true})
		let formated = []
		formated.push([nowLegal[0].from, [nowLegal[0].to]])
		for (let l in nowLegal) {
			for (let i=0; i <= formated.length-1; i++) {
				console.log(i)
				if (nowLegal[l].from == formated[i][0]){
					formated[i][1].push(nowLegal[l].to)
					break
				} else {
					if (i == formated.length-1) {
						formated.push([nowLegal[l].from, [nowLegal[l].to]])
					}
				}
			}
		}
		legal = new Map(formated);
		return legal
	}

	generateLegalMoves()
	updateConfig()

	//play()

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