<script lang="ts">
import { fetchUserData,getCookie } from "$lib/api";
import { userStore,type User } from "$lib/store";
import { DarkMode,Navbar,NavBrand,NavHamburger,NavLi,NavUl } from "flowbite-svelte";
import { onMount } from "svelte";
import '../app.css';


let userData: User | null = null;
let isLoggedIn = false;  // Assume that the user is not logged in at first

userStore.subscribe(d => userData = d)

onMount(() => {
	isLoggedIn = getCookie('isLoggedIn') === 'yes';
    fetchUserData(userData);
})

let btnClass: string = "text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5"

</script>


<!-- <DarkMode /> -->

<Navbar let:hidden let:toggle class="mb-5">
	<NavBrand href={isLoggedIn ? "/" : "/welcome"}>
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
		<NavLi class="mt-2" href="/logout">Logout</NavLi>
	</NavUl>
</Navbar>

<body class="bg-white dark:bg-gray-800 h-[100vh] dark:text-white">
	<slot />
</body>
