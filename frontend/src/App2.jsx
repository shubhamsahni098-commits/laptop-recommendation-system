import React, { useState } from 'react'
import './index.css'
import Input from './Input'
import Output from './Output'

export default function App() {

  const [budget, setBudget] = useState("")
  const [primaryUse, setPrimaryUse] = useState("")
  const [secondaryUse, setSecondaryUse] = useState("")
  const [laptops, setLaptops] = useState([])
  const [loading, setLoading] = useState(false)

  return (
    <>
      <h1 className='head'>Laptop Recommendation System</h1>
      <p className='para'>
        Get the best Laptops based on your budget and requirements
      </p>

      <Input
        budget={budget}
        setBudget={setBudget}
        primaryUse={primaryUse}
        setPrimaryUse={setPrimaryUse}
        secondaryUse={secondaryUse}
        setSecondaryUse={setSecondaryUse}
        setLaptops={setLaptops}
        setLoading={setLoading}
      />

      <Output
        laptops={laptops}
        loading={loading}
      />
    </>
  )
}