
import React ,{useState} from 'react'
import './index.css'
import Input from './Input'
import Output from './Output'

export default function App() {

  const [budget, setBudget] = useState("");
  const [primaryUse, setPrimaryUse] = useState("");
  const [secondaryUse, setSecondaryUse] = useState("");
  const [laptops, setLaptops] = useState([]);
  const [loading, setLoading] = useState(false)
  const [budgetError, setBudgetError] = useState("");
  const [primaryError, setPrimaryError] = useState("");
  const [secondaryError, setSecondaryError] = useState("");

  const getRecommendations = async () => {
    setBudgetError("");
    setPrimaryError("");

    let valid = true;

    // Budget validation
    if (!budget) {
        setBudgetError("*Please enter your budget.");
        valid = false;
    }
    else if (Number(budget) < 10000 || Number(budget) > 300000) {
        setBudgetError("*Budget must be between ₹10,000 and ₹3,00,000.");
        valid = false;
    }

    // Primary Use validation
    {/*if (primaryUse === "Select Primary Use") {
        setPrimaryError("Please select a primary use.");
        valid = false;
    }*/}

    if (!valid) return;
    
    try {
        setLoading(true);
        const response = await fetch("https://laptop-recommendation-api.onrender.com/recommend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                budget: Number(budget),

                primary_use: primaryUse,

                secondary_use: secondaryUse

            })

        });

        const data = await response.json();

        console.log(data);

        setLaptops(data);

    }

    catch(error){

        console.log(error);

    }
    finally{
      setLoading(false);
    }

}

  return (
    <>
     <div className={loading ? "app loading" : "app"}>
      <h1 className='head'>Laptop Recommendation System</h1>
      <p className='para'>Get the best Laptops based on your budget and requirements</p>
      <Input
       budget={budget}
       setBudget={setBudget}
       primaryUse={primaryUse}
       setPrimaryUse={setPrimaryUse}
       secondaryUse={secondaryUse}
      setSecondaryUse={setSecondaryUse}
      getRecommendations={getRecommendations}
      setLoading={setLoading}
      setLaptops={setLaptops}
      budgetError={budgetError}
      setBudgetError={setBudgetError}
      primaryError={primaryError}
     />
     {laptops.length>0?
     <p className='f-sz wh bld m-0 out-hd '>Top 5 Recommended Laptops</p>
     :null
    }
     </div>
      <Output laptops={laptops} loading={loading}/>
      
    </>
  )
}



