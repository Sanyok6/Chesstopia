import { userStore, type User } from "./store";

export const parseCookies = (cookieString: string, name: string) =>
  cookieString.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || null;

export const getCookie = (name: string) =>
  document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || null;

export const fetchApi = async (
  endpoint: string,
  options?: RequestInit,
  csrfTk?: string | null
): Promise<Response> => {
  const csrfToken = csrfTk ? csrfTk : getCookie('csrftoken');
  const defaultOptions = { ...options };

  defaultOptions.headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    ...defaultOptions.headers
  };

  if (csrfToken) {
    defaultOptions.headers = { 'X-CSRFToken': csrfToken, ...defaultOptions.headers };
  }
  defaultOptions.credentials = 'include';
  return await fetch('http://127.0.0.1:5173/api/' + endpoint, defaultOptions);
};

export const fetchUserData = (userData: User | null, csrfTk?: string) => {
  if (!userData && (getCookie('isLoggedIn') === 'yes')) {
    fetchApi("auth/users/me/", {}, csrfTk).then((response) => {
      if (response.ok) {
            response.json().then(j => userStore.set(j["user"]));
        }
    })
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const formatApiErrors = (data: any): Array<string> => {
  const messages: Array<string> = [];
  for (const [key, value] of Object.entries(data)) {
    messages.push(
      `${key !== 'detail' ? `${key}: ` : ''}${Array.isArray(value) ? value.join(', ') : value}`
    );
  }
  return messages;
};