/**
 * Root component holding all application state.
 */

import { useState } from 'react'
import { ThemeProvider, CssBaseline } from '@mui/material'
import theme from './theme'
import MunicipalityPicker from './components/MunicipalityPicker'
import SurfaceList from './components/SurfaceList'

export default function App() {
  const [step, setStep] = useState(1)
  const [municipalityId, setMunicipalityId] = useState('')
  const [surfaces, setSurfaces] = useState([])


  const handleSelect = id => {
    setMunicipalityId(id)
    setStep(2)
  }


  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {step === 1 && <MunicipalityPicker onSelect={handleSelect}></MunicipalityPicker>}
      {step === 2 && <SurfaceList surfaces={surfaces} onChange={setSurfaces}></SurfaceList>}
    </ThemeProvider>
  )
}
