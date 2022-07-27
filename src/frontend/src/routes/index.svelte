<script lang="ts">
import { fly } from 'svelte/transition';
import { Button } from "flowbite-svelte";
import { userStore, type User, type UserStats } from "$lib/store";


let userData: User | null = null;
let stats: UserStats | null = null;

userStore.subscribe((data) => {
    userData = data;
    stats = data?.stats || null;
});

let confusion_chess_btn = false
let magic_chess_btn = false
</script>


<div class="flex justify-center">
    <div class="w-[100vw] xl:w-[40vw]">
        <div class="flex items-center my-4 before:flex-1 before:border-t before:border-gray-300 before:mt-0.5 after:flex-1 after:border-t after:border-gray-300 after:mt-0.5">
            <p class="text-center font-semibold text-xl mx-4 mb-0 dark:text-white">
                {#if userData}
                    Play Chess 
                {:else}
                    Loading...
                {/if}
            </p>
        </div>

        <div class="flex justify-center">
            <div on:mouseenter={() => {confusion_chess_btn=true}} on:mouseleave={() => {confusion_chess_btn=false}} class="w-[100%] m-3">
                <Button class="w-[100%] h-60 lg:text-[35px] sm:text-[25px] overflow-hidden">
                    {#if confusion_chess_btn}
                        <img src="/confusion_chess.png" alt="" class="h-52" transition:fly="{{ y: 150, duration: 300 }}" />
                    {:else}
                        <div class="absolute" transition:fly="{{ y: -120, duration: 300 }}">Confusion Chess</div>
                    {/if}
                </Button>
            </div>

            <div on:mouseenter={() => {magic_chess_btn=true}} on:mouseleave={() => {magic_chess_btn=false}} class="w-[100%] m-3">
                <Button class="w-[100%] h-60 lg:text-[35px] sm:text-[25px] overflow-hidden">
                    {#if magic_chess_btn}
                        <img src="/magic_chess.png" alt="" class="h-52" transition:fly="{{ y: 150, duration: 300 }}" />
                    {:else}
                        <div class="absolute" transition:fly="{{ y: -120, duration: 300 }}">Magic Chess</div>
                    {/if}
                </Button>
            </div>
        </div>
    </div>

</div>

<div class="flex justify-center mt-36">
    <div class="lg:w-[40vw]">
        <div class="flex items-center my-4 before:flex-1 before:border-t before:border-gray-300 before:mt-0.5 after:flex-1 after:border-t after:border-gray-300 after:mt-0.5">
            <p class="text-center font-semibold text-xl mx-4 mb-0 dark:text-white">
            Your Stats
            </p>
        </div>

        {#if stats}
        <div class="flex justify-center text-left">
            <div class="w-[100%] m-3">
                <p class="text-2xl font-bold">Confusion chess</p>
                <p class="text-xl">Games Played: <span class="text-blue-500">{stats.confusion_chess.wins + stats.confusion_chess.losses + stats.confusion_chess.draws}</span></p>
                <p class="text-xl">Games Won: <span class="text-green-500">{stats.confusion_chess.wins}</span> </p>
                <p class="text-xl">Games Lost: <span class="text-red-500">{stats.confusion_chess.losses}</span> </p>
                <p class="text-xl">Games Drawn: <span class="text-yellow-500">{stats.confusion_chess.draws}</span> </p>
            </div>

            <div class="w-[100%] m-3">
                <p class="text-2xl font-bold">Magic chess</p>
                <p class="text-xl">Games Played: <span class="text-blue-500">{stats.magic_chess.wins + stats.magic_chess.losses + stats.magic_chess.draws}</span>  </p>
                <p class="text-xl">Games Won: <span class="text-green-500">{stats.magic_chess.wins}</span>  </p>
                <p class="text-xl">Games Lost: <span class="text-red-500">{stats.magic_chess.losses}</span>  </p>
                <p class="text-xl">Games Drawn: <span class="text-yellow-500">{stats.magic_chess.draws}</span>  </p>
            </div>
        </div>
        {:else}
            <h1 class="text-3xl text-center">Loading stats...</h1>
        {/if}
    </div>

</div>