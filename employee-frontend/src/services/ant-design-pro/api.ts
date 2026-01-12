import { request } from '@umijs/max';

const API_PREFIX = '/api/v1';

export async function currentUser(options?: { [key: string]: any }) {
  return request<API.CurrentUser>(`${API_PREFIX}/profile/`, {
    method: 'GET',
    ...(options || {}),
  });
}

export async function outLogin(body: { refresh: string }, options?: { [key: string]: any }) {
  return request<Record<string, any>>(`${API_PREFIX}/logout/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

export async function login(body: API.LoginParams, options?: { [key: string]: any }) {
  return request<API.LoginResult>(`${API_PREFIX}/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

// Demo table-list stubs to keep existing pages compiling.
export async function rule(
  _params: {
    current?: number;
    pageSize?: number;
  },
  _options?: { [key: string]: any },
) {
  return Promise.resolve<API.RuleList>({ data: [], total: 0, success: true });
}

export async function addRule(_options?: { [key: string]: any }) {
  return Promise.resolve<API.RuleListItem>({});
}

export async function updateRule(_options?: { [key: string]: any }) {
  return Promise.resolve<API.RuleListItem>({});
}

export async function removeRule(_options?: { [key: string]: any }) {
  return Promise.resolve<Record<string, any>>({ success: true });
}
