/**
 * API client — the only file that calls fetch().
 */

const BASE = import.meta.env.VITE_API_BASE ?? '/api'

export async function fetchMunicipalities() {
  const res = await fetch(`${BASE}/municipalities`)
  if (!res.ok) {
    throw new Error(`Error ${res.status} returned.`)
  } 
  return res.json()
}

export async function requestEstimate({ surfaces, municipality_id, address, parcel_area_sqft }) {
  const res = await fetch(`${BASE}/estimate`, {
    method: 'POST',
    headers:{ 'Content-Type': 'application/json' },
    body: JSON.stringify({ surfaces, municipality_id, address, parcel_area_sqft }),
  })
  if (!res.ok) {
    throw new Error(`Error ${res.status} returned`)
  }
  return res.json()
}
