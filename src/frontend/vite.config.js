import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api/ws/play/': {
				// WebSocket Proxy
				target: 'http://127.0.0.1:8000/',
				ws: true
			},
			'/api/': {
				target: 'http://127.0.0.1:8000/'
			}
		}
	},
	ssr: {
		noExternal: ['svelte-use-chessground', 'chessground']
	}
};

export default config;
