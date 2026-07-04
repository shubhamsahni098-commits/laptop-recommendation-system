import React from 'react'
import { FaMagic } from "react-icons/fa";
import './index.css'

export default function Input(props) {

  
  return (
    <>
      <div className='input flex wrap gap'>
        <div className='m-left in'>
            <h5 className='f-size fnt m-bt wh'>Budget (₹)</h5>
            <label>₹</label>
            <input
             className='ht'
             type="number"
             placeholder="Enter your budget"
             value={props.budget}
             min="10000"
             max="300000"
             onChange={(e) =>{ props.setBudget(e.target.value);
              props.setBudgetError("");
             }}
            />
            {props.budgetError && (
            <p className="error">{props.budgetError}</p>)}
        </div>
        <div className='m-let in'>
            <h5 className='f-size fnt m-bt wh'>Primary Use</h5>
            <label></label>
            <select
             className='ht-wd'
             value={props.primaryUse}
             onChange={(e) => props.setPrimaryUse(e.target.value)}
            >
              {props.primaryError && (
               <p className="error">{props.primaryError}</p>
              )}
              <option value="">Select Primary Use</option>
              <option value="gaming">Gaming</option>
              <option value="coding">Coding</option>
              <option value="office">Office Work</option>
        
            </select>
        </div>
        <div className='m-let in'>
            <h5 className='f-size m-bt fnt wh '>Secondary Use (Optional)</h5>
            <label></label>
            <select
             className='ht-wd'
             value={props.secondaryUse}
             onChange={(e) => props.setSecondaryUse(e.target.value)}
             >
              <option value="">Select Secondary Use</option>
              <option value="gaming">Gaming</option>
              <option value="coding">Coding</option>
              <option value="office">Office Work</option>
        
            </select>
        </div>
        
        <div className='bt flex cnt'>
            <button
              className='btn'
              onClick={props.getRecommendations}
             disabled={props.loading}
            >
           {props.loading ? "Loading..." : "✦ Recommend Laptops"}
            </button>
        </div>
        
       

      </div>
    </>
  )
}
