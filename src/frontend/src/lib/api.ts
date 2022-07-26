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
  return await fetch('http://localhost:5173/api/' + endpoint, defaultOptions);
};

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