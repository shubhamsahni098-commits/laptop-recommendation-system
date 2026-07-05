import React from 'react'

import './index.css'

export default function LaptopCards(props) {
  return (
    <>
    <div className='lap-card'>
      <img className='ht-img ' src={props.laptop.image} alt={props.laptop.name}
       onError={(e) => {
      e.target.onerror = null;
     e.target.src = lp;
     }}/>
      <p className='m-l f-size bld wh fnt m-0'>{props.laptop.name}</p>
      <div className='r m-top' >
        <p className='m-0 m-lt2 gr'>{props.laptop.processor}</p>
        <p className='m-0 m-lt2 gr'>{props.laptop.memory}</p>
        <p className='m-0 m-lt2 gr'>{props.laptop.graphics}</p>
      </div>
        <div className="price-row">
          <p className="price">
            ₹{props.laptop.price.toLocaleString("en-IN")}
         </p>

          <p className="stars">★★★★★</p>
        </div>
    </div>
    
    
    </>
  )
}
