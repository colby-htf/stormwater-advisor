/**
 * Root component holding all application state.
 */

import { useState } from 'react'
import { ThemeProvider, CssBaseline, Box, TextField, Button } from '@mui/material'
import theme from './theme'
import MunicipalityPicker from './components/MunicipalityPicker'
import SurfaceList from './components/SurfaceList'
import { requestEstimate } from './api/client'

export default function App() {
  const [step, setStep] = useState(1)
  const [municipalityId, setMunicipalityId] = useState('')
  const [surfaces, setSurfaces] = useState([])
  const [address, setAddress] = useState('')
  const [parcelAreaSqft, setParcelAreaSqft] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)


  const handleSelect = id => {
    setMunicipalityId(id)
    setStep(2)
    
  }

  const handleCalculate = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await requestEstimate({ surfaces: surfaces.map(s => {
        const { id, ...rest} = s
        return { ...rest, area_sqft: parseFloat(s.area_sqft)}
      }), municipality_id: municipalityId, address: address, parcel_area_sqft: parseFloat(parcelAreaSqft) })
      setResult(data)
      setStep(3)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
      
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {step === 1 && <MunicipalityPicker onSelect={handleSelect}></MunicipalityPicker>}
      {step === 2 && (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField label="Address" value={address} onChange={event => setAddress(event.target.value)}></TextField>
          <TextField type="number" label="Parcel area (sq ft)" value={parcelAreaSqft} onChange={event => setParcelAreaSqft(event.target.value)}></TextField>
          <SurfaceList surfaces={surfaces} onChange={setSurfaces} />
          <Button variant="contained" onClick={handleCalculate}>Calculate Estimate</Button>
        </Box>
      )}
      {step === 3 && <p><p>{JSON.stringify(result)}</p></p>}
    </ThemeProvider>
  )

}
