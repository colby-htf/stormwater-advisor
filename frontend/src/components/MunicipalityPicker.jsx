/**
 * Municipality selector dropdown.
 */

import { useState, useEffect } from "react"
import { fetchMunicipalities } from "../api/client"
import { CircularProgress, Alert, MenuItem, Select, Button } from '@mui/material';



export default function MunicipalityPicker({ onSelect }) {
  const [municipalities, setMunicipalities] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState("")

  useEffect(() => {
    fetchMunicipalities()
      .then(setMunicipalities)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <CircularProgress />
  if (error) return <Alert severity="error">Unable to retrieve municipality data.</Alert>

  return (
    <>
      <Select value={selected} onChange={event => setSelected(event.target.value)}>
        {municipalities.map(m => (
          <MenuItem key={m.municipality_id} value={m.municipality_id}>{m.display_name}</MenuItem>
        ))}
      </Select>
      <Button variant="contained" disabled={selected === ""} onClick={() => onSelect(selected)}>Next</Button>
    </>

  )

}
