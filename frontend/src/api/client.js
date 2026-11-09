/**
 * API client — the only file that calls fetch().
 */

const BASE = import.meta.env.VITE_API_BASE ?? '/api'

export async function fetchMunicipalities() {
  const res = await fetch(`${BASE}/municipalities`)
  if (!res.ok) {
    throw new Error(`Error ${res.status} returned.`)
  } return res.json()
  }

export async function requestEstimate({ surfaces, municipalityId }) {
  // TODO — Issue #21
  throw new Error('Not implemented')
}
