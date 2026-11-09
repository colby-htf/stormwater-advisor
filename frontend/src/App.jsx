/**
 * Root component holding all application state.
 */

import { useState } from 'react'
import { ThemeProvider, CssBaseline } from '@mui/material'
import theme from './theme'
import MunicipalityPicker from './components/MunicipalityPicker'

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <MunicipalityPicker onSelect={id => console.log(id)} />
    </ThemeProvider>
  )
}
