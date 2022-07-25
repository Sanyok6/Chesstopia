<script>
	import { DarkMode, Navbar, NavBrand, NavHamburger, NavLi, NavUl } from "flowbite-svelte";
	import '../app.css';
</script>


<!-- <DarkMode /> -->

<Navbar let:hidden let:toggle class="mb-5">
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
			Chesstopia
		</span>
	</NavBrand>
	<div>
		<DarkMode />
		<NavHamburger on:click={toggle} />
	</div>

	<NavUl {hidden}>
		<NavLi href="dashboard">Play</NavLi>
		<NavLi href="#">About</NavLi>
		<NavLi href="#">Settings</NavLi>
		<NavLi href="#">Logout</NavLi>
	</NavUl>
</Navbar>

<body class="bg-white dark:bg-gray-800 h-[100vh] dark:text-white">
	<slot />
</body>
