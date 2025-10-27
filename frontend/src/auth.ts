import { api, setAuthToken } from './api'

export async function login(username: string, password: string) {
  const { data } = await api.post('/api/auth/login/', { username, password })
  setAuthToken(data.access)
  return data.user
}

export async function register(payload: any) {
  const { data } = await api.post('/api/auth/register/', payload)
  return data
}

export async function passwordReset(email: string) {
  const { data } = await api.post('/api/auth/password-reset/', { email })
  return data
}
