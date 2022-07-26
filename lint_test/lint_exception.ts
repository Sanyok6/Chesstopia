
import { writable } from 'svelte/store';

interface User {
    id: number;
    username: string;
    is_staff: boolean;
}

export const userStore = writable<User | null>(null);
