import React from 'react'
import './index.css'
import LaptopCards from './LaptopCards'

export default function Output(props) {
  return (
    <>
      <div className='output'>
        {/*<div className='flex gapx rel srt'>
          {props.laptops.length >0?(
            <p className='f-sz wh bld m-0 txt-und '>Top 5 Recommended Laptops</p>):null}
            
        </div>*/}
        
        
        {props.loading ? (
          <>
           <div className="loader"></div>
           <p className=' txt-cnt wh m-top med'>Prices are subject to change. Please verify before purchasing</p>
          </> 
         ) : props.laptops.length > 0 ? (
          <div className="lp flex">
           {props.laptops.map((laptop, index) => (
            <LaptopCards key={index} laptop={laptop} />
         ))}
        </div>
        ) : null}
        
        
      </div>
      
    </>
  )
}
