import { writable } from 'svelte/store';

export interface UserStats {
	confusion_chess: { wins: number; losses: number; draws: number };
	magic_chess: { wins: number; losses: number; draws: number };
}

export interface User {
	id: number;
	username: string;
	is_staff: boolean;
	is_playing: boolean;
	stats: UserStats;
}

export const userStore = writable<User | null>(null);

export interface Appearance {
	board_style: string;
	piece_set: string;
}

export const appearanceStore = writable<Appearance | null>(null);
