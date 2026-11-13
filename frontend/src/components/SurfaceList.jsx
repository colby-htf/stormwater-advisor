/**
 * Dynamic list of surface entries with add/remove functionality.
 */
import { Button, TextField, MenuItem } from "@mui/material"


const SURFACE_KINDS = [
  { value: "roof", label: "Roof" },
  { value: "driveway", label: "Driveway" },
  { value: "walkway", label: "Walkway" },
  { value: "patio", label: "Patio" },
  { value: "parking_lot", label: "Parking Lot" },
  { value: "pool_deck", label: "Pool Deck" },
  { value: "lawn", label: "Lawn" },
]

const SURFACE_MATERIALS = [
  { value: "asphalt", label: "Asphalt" },
  { value: "concrete", label: "Concrete" },
  { value: "pavers", label: "Pavers" },
  { value: "shingle", label: "Shingle" },
  { value: "metal", label: "Metal" },
  { value: "gravel", label: "Gravel" },
  { value: "turf", label: "Turf" },
  { value: "pervious_concrete", label: "Pervious Concrete" },
  { value: "porous_asphalt", label: "Porous Asphalt" },
  { value: "permeable_pavers", label: "Permeable Pavers" },
  { value: "grass_grid", label: "Grass Grid" },
]

export function SurfaceRow({ surface, onChange, onRemove }) {
  return (
    <>
      <TextField select label="Kind" value={surface.kind} onChange={event => onChange(surface.id, { kind: event.target.value })}>
        {SURFACE_KINDS.map(k => (
          <MenuItem key={k.value} value={k.value}>{k.label}</MenuItem>
        ))}
      </TextField>
      <TextField select label="Material" value={surface.material} onChange={event => onChange(surface.id, { material: event.target.value })}>
        {SURFACE_MATERIALS.map(m => (
          <MenuItem key={m.value} value={m.value}>{m.label}</MenuItem>
        ))}
      </TextField>
      <TextField
        type="number"
        label="Area (sq ft)"
        value={surface.area_sqft}
        onChange={event => onChange(surface.id, { area_sqft: event.target.value })}
      />
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
  )
}
