<script lang="ts">
    import { Alert } from "flowbite-svelte";
    import { goto } from "$app/navigation";
    import { fetchApi,formatApiErrors,getCookie } from "../lib/api";
    import { userStore } from "$lib/store";

    let messages: string[] = [];

    let username: string;
    let password: string;

    const handleLogin = async () => {
        const response = await fetchApi("auth/login/", {
            method: "POST",
            body: JSON.stringify({
                username,
                password
            })
        });

        if (response.ok) {
            console.info("login successful");
            goto("/");
        } else {
            const errors = formatApiErrors(await response.json()); // this will be a list of strings
            console.error(errors)
            messages=errors;
            // TODO: Show API errors
        }
    }
</script>

<div class="min-h-[75%] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h1 class="text-6xl font-extralight text-center">Chesstopia</h1>
        <h2 class="mt-8 text-center text-3xl font-semibold text-gray-700 dark:text-gray-400">Login in to your account</h2>
      </div>
      <form class="mt-5 space-y-6" on:submit|preventDefault={handleLogin}>
        {#if messages.length}
          <Alert color="yellow">{messages.toString()}</Alert>
        {/if}
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">Email address</label>
            <input id="username" bind:value={username} name="uername" type="username" autocomplete="username" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Username">
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input id="password" name="password" bind:value={password} type="password" autocomplete="current-password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password">
          </div>
        </div>
    
        <div>
          <button type="submit"
          class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          on:submit|preventDefault={handleLogin}>
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
            </span>
            Login
          </button>
        </div>
      </form>
    </div>
  </div>