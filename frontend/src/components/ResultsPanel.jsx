/**
 * Display estimated fees and pervious pavement alternatives.
 */

import { Box, Typography } from '@mui/material'

const formatter = new Intl.NumberFormat('en-us', {
  style: 'currency',
  currency: 'USD',
})

const formatCurrency = value => {
  if (value == null || value === '') {
    return '-'
  }
  return formatter.format(parseFloat(value))
}

export default function ResultsPanel({ result }) {
  if (!result) return null
  return (
    <Box sx={{
      display: 'flex',
      gap: 2
    }}>
      <Box>
        <Typography variant="body2">Estimated Fee Today</Typography>
        <Typography variant="h4">{formatCurrency(result.baseline.annual_fee)}</Typography>
      </Box>
      <Box>
        <Typography variant="body2">Estimated Fee with Swaps</Typography>
        <Typography variant="h4">{formatCurrency(result.proposed.annual_fee)}</Typography>
      </Box>
      <Box display='flex' justifyContent='space-between'>
        <Typography></Typography>
        
      </Box>
    </Box>

  )
}
