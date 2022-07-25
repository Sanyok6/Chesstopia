import { parseCookies } from '$lib/api';
import type { RequestEvent, ResolveOptions } from '@sveltejs/kit';
import type { MaybePromise } from '@sveltejs/kit/types/private';

interface HandlerArguments {
  event: RequestEvent;
  resolve(event: RequestEvent, opts?: ResolveOptions): MaybePromise<Response>;
}

export async function handle({ event, resolve }: HandlerArguments) {
  const url = event.url.pathname;
  const authEndpoints = ['/login', '/signup', '/welcome'];
  const isLoggedIn = parseCookies(event.request.headers.get('cookie') || '', 'sessionid');

  if (isLoggedIn) {
    // Response.redirect('/endpoint') doesn't work for some reason
    if (authEndpoints.includes(url)) {
      event.url.pathname = '/';
      return Response.redirect(event.url);
    }
  } else {
    if (!authEndpoints.includes(url)) {
      event.url.pathname = '/welcome';
      return Response.redirect(event.url);
    }
  }

  const response = await resolve(event);
  return response;
}

