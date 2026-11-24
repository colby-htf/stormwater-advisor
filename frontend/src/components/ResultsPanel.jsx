/**
 * Display estimated fees and pervious pavement alternatives.
 */

import {
  Box,
  Link,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material'

const formatterCurrency = new Intl.NumberFormat('en-us', {
  style: 'currency',
  currency: 'USD',
})

const formatCurrency = value => {
  if (value == null || value === '') {
    return '-'
  }
  return formatterCurrency.format(parseFloat(value))
}

const formatterYears = new Intl.NumberFormat('en-us', {
  style: 'unit',
  unit: 'year',
  unitDisplay: 'long',
  maximumFractionDigits: 1,
})

const formatYears = value => {
  if (value == null || value === '') {
    return '-'
  }
  return formatterYears.format(value)
}

const formatterArea = new Intl.NumberFormat('en-us', {
  maximumFractionDigits: 2,
})

const formatArea = value => {
  if (value == null || value === '') {
    return '-'
  }
  return formatterArea.format(value)
}

const formatterESU = new Intl.NumberFormat('en-us', {
  maximumFractionDigits: 2,
})

const formatESU = value => {
  if (value == null || value === '') {
    return '-'
  }
  return formatterESU.format(value)
}

// "porous_asphalt" -> "porous asphalt"
const formatMaterial = value => {
  if (value == null || value === '') {
    return '-'
  }
  return value.replaceAll('_', ' ')
}

export default function ResultsPanel({ result }) {
  if (!result) return null
  return (
    <Box>
      <Box display='flex' gap={5}>
        <Box>
          <Typography variant='body2'>Estimated Fee Today</Typography>
          <Typography variant='h4'>{formatCurrency(result.baseline.annual_fee)}</Typography>
          <Typography variant='body2'>
            {formatArea(result.baseline.impervious_sqft)} sq ft billed at {formatESU(result.baseline.billed_esu_count)} ESU
          </Typography>
        </Box>
        <Box>
          <Typography variant='body2'>Estimated Fee with Swaps</Typography>
          <Typography variant='h4'>{formatCurrency(result.proposed.annual_fee)}</Typography>
          <Typography variant='body2'>
            {formatArea(result.proposed.impervious_sqft)} sq ft billed at {formatESU(result.proposed.billed_esu_count)} ESU
          </Typography>
        </Box>
      </Box>

      <Box mt={3}>
        <Box display='flex' justifyContent='space-between'>
          <Typography variant='body2'>Annual Savings</Typography>
          <Typography variant='body1'>{formatCurrency(result.annual_savings)}</Typography>
        </Box>
        <Box display='flex' justifyContent='space-between'>
          <Typography variant='body2'>Upfront Cost</Typography>
          <Typography variant='body1'>{formatCurrency(result.upfront_cost_delta)}</Typography>
        </Box>
        <Box display='flex' justifyContent='space-between'>
          <Typography variant='body2'>Simple Payback</Typography>
          <Typography variant='body1'>{formatYears(result.simple_payback_years)}</Typography>
        </Box>
      </Box>

      <Box mt={3}>
        <Typography variant='body1'>Pervious pavement options</Typography>
        {result.options.length === 0 ? (
          <Typography variant='body2'>
            No pervious alternatives for these surfaces.
          </Typography>
        ) : (
          <Table size='small'>
            <TableHead>
              <TableRow>
                <TableCell>Surface</TableCell>
                <TableCell>Swap</TableCell>
                <TableCell align='right'>Area (sq ft)</TableCell>
                <TableCell align='right'>Upfront cost</TableCell>
                <TableCell align='right'>Savings per year if swapped alone</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {result.options.map((option, index) => (
                <TableRow key={index}>
                  <TableCell>{option.surface_label}</TableCell>
                  <TableCell>
                    {formatMaterial(option.from_material)} to {formatMaterial(option.to_material)}
                  </TableCell>
                  <TableCell align='right'>{formatArea(option.area_sqft)}</TableCell>
                  <TableCell align='right'>{formatCurrency(option.upfront_cost_delta)}</TableCell>
                  <TableCell align='right'>{formatCurrency(option.annual_fee_savings)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Box>

      <Typography variant='body1' sx={{ mt: 3 }}>
        Disclaimer: This is a planning estimate, not a bill or a permit determination.
        Actual fees are based on local municipality code and may differ from these figures.
      </Typography>
      <Typography variant='body2' sx={{ mt: 1 }}>
        <Link href={result.rate_source_url} target='_blank' rel='noopener'>
          Rate source
        </Link>
        , last verified {result.rate_verified_on}
      </Typography>
    </Box>
  )
}