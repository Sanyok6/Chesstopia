<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    const gameID = $page.params.id

	import { Range, Dropdown, DropdownItem, Input, Label, Button, Spinner, Toast, AccordionItem } from 'flowbite-svelte'

	let board_size = 50
	let board_style = "blue"

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

    let to_move = "white"
    let result = 2 //who cares bro

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
import { not_equal } from 'svelte/internal';
	const chess = new Chess()

	function play(from: string, to: string) {
		chess.move({ from: from, to: to, promotion: "q" })
        to_move = chess.turn() == "w" ? "white" : "black"
		if (!chess.gameOver()) {
			const moves = chess.moves()
			const move = moves[Math.floor(Math.random() * moves.length)]
			chess.move(move)
			fen=chess.fen()

			generateLegalMoves()
			
			updateConfig()
			//setTimeout(play, 10)
		} else {onGameOver()}
	}

	function generateLegalMoves() {
		const nowLegal = chess.moves({verbose:true})
		let formated = []
		formated.push([nowLegal[0].from, [nowLegal[0].to]])
		for (let l in nowLegal) {
			for (let i=0; i <= formated.length-1; i++) {
				//console.log(i)
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

    function onGameOver() {
        if (chess.inCheckmate()) {
            if (chess.turn() == "w") {
                result = -1
            } else {
                result = 1
            }
        } else {
            result = 0
        }
    }

	generateLegalMoves()
	updateConfig()

	//play()

    let game_started = true

    let game_url = ""
    onMount(() => game_url = window.location.href)

</script>

  
<div id="popup-modal" tabindex="-1" class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 md:inset-0 h-modal md:h-full justify-center items-center flex" aria-modal="true" role="dialog">
      <div class="relative p-4 w-full max-w-md h-full md:h-auto">
          <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
              <div class="p-6 text-center">
                  <h2 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-200">Waiting For Opponent</h2>
                  <div class='mb-6'>
                    <Label for='game-link' class='block mb-2'>Share is game link with your opponent:</Label>
                    <Input id="game-link" size="md" value={game_url} disabled />
                    <Spinner class="mt-10" size="12"></Spinner>
                  </div>
              </div>
          </div>
      </div>
  </div>

<div class="xl:grid grid-cols-3">
	<div class="col-span-2 flex justify-center items-center">
		<div
			style="width:{board_size}%;aspect-ratio:1"
			use:Chessground={{config, initializer}}
			use:cgStylesHelper="{{ piecesFolderUrl: '/game/pieces/', boardUrl: '/game/board_'+board_style+'.svg' }}"
		/>
	</div>	

	<div class="">
        <AccordionItem id="1">
            <h2 slot="header">Settings</h2>
            <div slot="body">
                <div class="m-3">
                    Adjust Board Size
                    <Range step={2} size="small" id="range1" min={25} max={95} bind:value={board_size}/>
                </div>
                <div class="m-3">
                    Board Theme
                    <Dropdown label="Board Theme" class="w-40">
                        <DropdownItem on:click={() => {board_style="blue"}}>Blue</DropdownItem>
                        <DropdownItem on:click={() => {board_style="green"}}>Green</DropdownItem>
                        <DropdownItem on:click={() => {board_style="brown"}}>Brown</DropdownItem>
                    </Dropdown>
                </div>
                <div class="m-3">
                    Piece Set
                    <Dropdown label="Piece Set" class="w-32">
                        <DropdownItem>Default</DropdownItem>
                    </Dropdown>
                </div>
            </div>
        </AccordionItem>
        <div class="text-center mt-5">
            <p class="text-3xl">Confusion Chess</p>
            <p class="text-lg">Opponent: Bob</p>

            <div class="flex items-center justify-center mt-4">
                {#if result == 2}
                    <img src="/game/pieces/{to_move.charAt(0)}K.svg" alt="{to_move} to move" class="w-12 h-12" />
                    <p class="text-lg">{to_move}'s move</p>   
                {/if}

                {#if result == 0}
                    <p class="text-xl">Game is a drawn</p>
                {/if}
                {#if result == 1}
                    <p class="text-xl">Game over, white won</p>
                {/if}
                {#if result == -1}
                    <p class="text-xl">Game over, black won</p>
                {/if}
            </div>
        </div>
    </div>
</div>