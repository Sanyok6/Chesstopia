<script lang="ts">
import { DarkMode, Navbar, NavBrand, NavHamburger, NavLi, NavUl } from "flowbite-svelte";
import { onMount } from "svelte";
import { fetchUserData } from "$lib/api";
import { userStore, type User } from "$lib/store";
import '../app.css';


let userData: User | null = null

userStore.subscribe(d => userData = d)

onMount(() => {
    fetchUserData(userData);
})

let btnClass: string = "text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5"

</script>


<!-- <DarkMode /> -->

<Navbar let:hidden let:toggle class="mb-5">
	<NavBrand href="/welcome">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			Chesstopia
		</span>
	</NavBrand>
	<div>
		
		<NavHamburger on:click={toggle} />
	</div>

	<NavUl {hidden}>
		<DarkMode {btnClass} />
		<NavLi class="mt-2" href="/">Play</NavLi>
		<NavLi class="mt-2" href="/about">About</NavLi>
		<NavLi class="mt-2" href="#">Settings</NavLi>
		<NavLi class="mt-2" href="#">Logout</NavLi>
	</NavUl>
</Navbar>

<body class="bg-white dark:bg-gray-800 h-[100vh] dark:text-white">
	<slot />
</body>
