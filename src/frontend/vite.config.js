import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	server: {
		proxy: {
		  '/api/': {
			target: 'http://127.0.0.1:8000/'
		  }
		}
	}
};

export default config;
