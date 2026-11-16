/**
 * Root component holding all application state.
 */

import { useState } from 'react'
import { ThemeProvider, CssBaseline, Box, TextField, Button } from '@mui/material'
import theme from './theme'
import MunicipalityPicker from './components/MunicipalityPicker'
import SurfaceList from './components/SurfaceList'

export default function App() {
  const [step, setStep] = useState(1)
  const [municipalityId, setMunicipalityId] = useState('')
  const [surfaces, setSurfaces] = useState([])
  const [address, setAddress] = useState('')
  const [parcelAreaSqft, setParcelAreaSqft] = useState('')
  const [result, setResult] = useState(getBottomNavigationActionUtilityClass)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)


  const handleSelect = id => {
    setMunicipalityId(id)
    setStep(2)
  }

  const handleCalculate = () => {}

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {step === 1 && <MunicipalityPicker onSelect={handleSelect}></MunicipalityPicker>}
      {step === 2 && (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField label="Address" value={address} onChange={setAddress}></TextField>
          <TextField type="number" label="Parcel area (sq ft)" value={parcelAreaSqft} onChange={setParcelAreaSqft} ></TextField>
          <SurfaceList surfaces={surfaces} onChange={setSurfaces} />
          <Button variant="contained" onClick={handleCalculate}>Calculate estimate</Button>
        </Box>
      )}
    </ThemeProvider>
  )
}
