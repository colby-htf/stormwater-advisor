/**
 * Dynamic list of surface entries with add/remove functionality.
 */
import { Button, TextField } from "@mui/material"

export function SurfaceRow({ surface, onChange, onRemove }) {
  return (
    <>
      <TextField value={surface.label} label="Label" onChange={event => onChange(surface.id, { label: event.target.value })}></TextField>
      <Button variant="contained" onClick={() => onRemove(surface.id)}>Remove</Button>
    </>
  )
}

export default function SurfaceList({ surfaces, onChange }) {
  const addSurface = () => {
    const newRow = { id: crypto.randomUUID(), kind: '', material: '', area_sqft: '', label: '' }
    onChange([...surfaces, newRow])
  }
  const removeSurface = id => {
    onChange(surfaces.filter(s => s.id !== id))
  }
  const updateSurface = (id, changes) => {
    onChange(surfaces.map(s => s.id === id ? { ...s, ...changes } : s))
  }

  return (
    <div>
      <Button variant="contained" onClick={addSurface}>Add surface</Button>
      {surfaces.map(surface => (
        <SurfaceRow key={surface.id} surface={surface} onChange={updateSurface} onRemove={removeSurface}></SurfaceRow>
      ))}
    </div>
)}
