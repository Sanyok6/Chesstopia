
import { writable } from 'svelte/store';

export interface User {
    id: number;
    username: string;
    is_staff: boolean;
}

export const userStore = writable<User | null>(null);


export interface Appearance {
    board_style: string;
    piece_set: string;
}

export const appearanceStore = writable<Appearance | null>(null);