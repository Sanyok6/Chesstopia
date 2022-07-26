
import { writable } from 'svelte/store';

export interface User {
    id: number;
    username: string;
    is_staff: boolean;
}

export const userStore = writable<User | null>(null);