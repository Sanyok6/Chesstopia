<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    const gameID = $page.params.id

    let userData: User | null = null;
        
    import { fetchApi } from '$lib/api';
    import { userStore } from '$lib/store';
    
    userStore.subscribe((data) => {
        userData = data;
    });

	import { Range, Dropdown, DropdownItem, Input, Label, Spinner, AccordionItem } from 'flowbite-svelte'

	let board_size = 50
	let board_style = "blue"

    let playerColor = ""

    let opponentName = ""

	import { Chessground, cgStylesHelper } from 'svelte-use-chessground';
	import 'svelte-use-chessground/cgstyles/chessground.css';

    let to_move = "white"
    let result = 2 //who cares bro

	let fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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
        lastMove: [],
        orientation: "white",
	};

	const updateConfig = () => {
		config.movable.dests = legal
		config.fen = fen
	}


	function initializer(api: any) {
		cgApi = api;
	}

	import { Chess } from 'chess.ts'

	const chess = new Chess(fen)

	function play(from: string, to: string) {
		// chess.move({ from: from, to: to, promotion: "q" })
        let backup_fen = chess.fen()
        
        chess.put(chess.remove(from), to)
        
        let f = chess.fen().split(" ")
        if (f[1] == "w") {
            to_move = "black"
        } else {
            to_move = "white"
        }
        console.log(chess.fen())
        if (!chess.load(f[0]+" "+to_move.charAt(0)+" "+f[2]+" "+f[3]+" "+f[4]+" "+f[5])) {
            chess.load(backup_fen)
            fen=backup_fen
            updateConfig()
            generateLegalMoves()
            if (!chess.load(f[0]+" "+to_move.charAt(0)+" "+f[2]+" - "+f[4]+" "+f[5])) {
                return
            }
        }
		if (!chess.gameOver()) {
			const moves = chess.moves()
			const move = moves[Math.floor(Math.random() * moves.length)]
			chess.move(move)
			fen=chess.fen()

			//generateLegalMoves()
            to_move = "white"
			ability = getAbilityCard()

			updateConfig()
		} else {onGameOver()}
	}

	function generateLegalMoves(f=[]) {
		const nowLegal = chess.moves({verbose:true}).concat(f)
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
        console.log("game over, result: "+result)
    }

    let game_started = false 

    let game_url = ""
    onMount(() => game_url = window.location.href)

    const connect = () => {
        let ws = new WebSocket(
            'ws://'
            + window.location.host
            + '/api/ws/play/'
            + gameID
            + '/'
        );

        ws.onopen = () => {
            console.log('connected')
        };

        ws.onmessage = (message) => {
            message = JSON.parse(message.data)
            console.log(message)
            if (message.event == "CREATE_MOVE") {
    
                let backup_fen = chess.fen()
        
                chess.put(chess.remove(message.payload.from), message.payload.to)
                
                let f = chess.fen().split(" ")
                if (f[1] == "w") {
                    to_move = "black"
                } else {
                    to_move = "white"
                }
                console.log(chess.fen())
                if (!chess.load(f[0]+" "+to_move.charAt(0)+" "+f[2]+" "+f[3]+" "+f[4]+" "+f[5])) {
                    chess.load(f[0]+" "+to_move.charAt(0)+" "+f[2]+" - "+f[4]+" "+f[5])
                }

                fen = chess.fen()

                // chess.move({ from: message.payload.from, to: message.payload.to, promotion: message.payload.promotion })
                // fen = chess.fen()

                // to_move = chess.turn() == "w" ? "white" : "black"

                if (chess.gameOver()) {
                    onGameOver()
                    ws.send(JSON.stringify({action: "SET_RESULT", data: {result: result}}))
                } else if (chess.turn() == playerColor) {
                    if (chess.inCheck()) {
                        generateLegalMoves()
                    } else {
                        ability = getAbilityCard()
                    }
                } else {
                    legal = new Map([])
                }
                
                updateConfig()
                config.lastMove = [message.payload.from, message.payload.to]


            } else if (message.event == "GAME_START") {
                console.log("starting game")

                setTimeout(() => {
                    game_started = true
                    if (message.payload.white.id == userData.id) {
                        playerColor = "w"
                        config.orientation = "white"
                        opponentName = message.payload.black.username
                        ability = getAbilityCard()
                    } else if (message.payload.black.id == userData.id) {
                        playerColor = "b"
                        config.orientation = "black"
                        opponentName = message.payload.white.username
                    } else {console.log("You are not a member of this game, please leave.")}
                    console.log("playing as "+playerColor)

                    //chess.load(message.payload.starting_pos)
                    //fen = message.payload.starting_pos
                    updateConfig()
                }, 1000)

            }
        };

        config.movable.events = {after: (from, to) => (
            ws.send(JSON.stringify({
                "action": "MAKE_MOVE",
                "data": {"from": from, "to": to, "promotion": "q"}
            }))
        )}
        
    }

    onMount(() => {
        connect()
    })


    const get_piece_positions = (game, piece) => {
        return [].concat(...game.board()).map((p, index) => {
            if (p !== null && p.type === piece.type && p.color === piece.color) {
            return index
            }
        }).filter(Number.isInteger).map((piece_index) => {
            const row = 'abcdefgh'[piece_index % 8]
            const column = Math.ceil((64 - piece_index) / 8)
            return row + column
        })
    }

    function validateMagicChessMoves(piece:{type:string;color:string;}) {

        function validate(pieceType: {type:string;color:string;}, square:string) {
            // Creates a new instance of chess game to calculate moves
            const c = new Chess("8/8/8/8/8/8/8/8 "+pieceType.color+" - - 0 1");
            c.put({ type: pieceType.type, color: pieceType.color }, square); // to_move.charAt(0)

            console.log("color "+piece.color+" to move "+c.turn()+ " given fen"+c.fen())
            const moves = c.moves({verbose: true});
            console.log(moves)
            // by default first char is the piece type, last char is # if the move causes checkmate
            // stripping both for now.
            //return moves.map(move => (move.slice(1)).replace('#', ""));
            return moves
        }

        const pieceType = piece
        const square = get_piece_positions(chess, piece)

        if (square == []) {return}

        const magicMoves = validate(pieceType, square[0]);
        console.log(magicMoves);

        generateLegalMoves(magicMoves)
    }


    function getAbilityCard() {
        const pieces = ["p", "b", "r", "q"]
        const piece = pieces[Math.floor(Math.random() * pieces.length)]

        console.log(to_move.charAt(0))

        validateMagicChessMoves({type: piece, color: to_move.charAt(0)})

        let title = ""
        let description = ""
        let image = ""

        switch (piece) {
            case "p":
                title = "Super Pawn"                
                description = "You can move your pawn one square forward, even if there is an enemy piece there."
                image = "/game/pieces/wP.svg"
                break;
            case "b":
                title = "Super Bishop"
                description = "One of your bishops can move diagonally to any square, even if it takes or passes an enemy piece."
                image = "/game/pieces/wB.svg"
                break;
            case "r":
                title = "Magic Rook"
                description = "One of your rooks can move horizontally or vertically to any square, even if it takes or passes an enemy piece."
                image = "/game/pieces/wR.svg"
                break;
            case "q":
                title = "Magic Queen"
                description = "Your queen can move horizontally, vertically, or diagonally to any square, even if it takes or passes an enemy piece."
                image = "/game/pieces/wQ.svg"
                break;
        
            default:
                break;
        }

        return {title: title, description: description, image: image}
    }

    let ability = getAbilityCard()

    //generateLegalMoves([["h2", ["h8"]]])
    //validateMagicChessMoves({type: "b", color: to_move.charAt(0)})
    updateConfig()

</script>

{#if !game_started}
<div id="popup-modal" tabindex="-1" class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 md:inset-0 h-modal md:h-full justify-center items-center flex" aria-modal="true" role="dialog">
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
{/if}

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
            <p class="text-lg">Opponent: {opponentName}</p>

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

            <div class="flex items-center justify-center mt-4 ">
                {#if (to_move.charAt(0) == playerColor && !chess.inCheck())}
                <div class="w-[50%] h-60 rounded-lg bg-[#ededed] dark:bg-black p-5">
                    <h1 class="text-xl my-2">{ability.title}</h1>
                    {ability.description}
                    <div class="flex items-center justify-center my-3">
                        <img src={ability.image} alt="" class="w-12 h-12" />
                    </div>
                </div>
                {/if}
            </div>
        </div>
    </div>
</div>