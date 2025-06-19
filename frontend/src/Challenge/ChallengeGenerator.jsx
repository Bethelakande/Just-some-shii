import "react"
import { useState, useEffect } from "react"
import { MCQChallenge } from "./MCQChallenge"
import { useApi } from "../utils/api"

export function ChallengeGenerator() {
    const [Challenge, setChallenge] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)
    const [difficulty, setDifficulty] = useState("easy")
    const [quota, setQuota] = useState(null)

    const {makeRequest} = useApi()

    useEffect(() => {
        fetchQuota()
    }, [])
    
    const fetchQuota = async() => {
        try {
            const response = await makeRequest("quota")
            console.log('response quota: ', response)
            setQuota(response?.quota)
        } catch (error) {
            console.error("Error fetching quota:", error)
            setError(error.message)
        } finally {
            setIsLoading(false)
        }
    }


    const generateChallenge = async() => {
        setIsLoading(true)
        setError(null)

        try{
            const data = await makeRequest("create_challenge",{
                method: "POST",
                body: JSON.stringify({
                    difficulty
                })
            })
            console.log(`data: ${data}`)
            setChallenge(data)
            fetchQuota()
        } catch (error) {
            console.error("Error generating challenge:", error)
            setError(error.message || "Failed to generate challenge")
        } finally {
            setIsLoading(false)
        }
    }
    
    const getNextResetTime = () =>{
        if (!quota?.last_reset_date){
            return "N/A"
        }
        const lastResetDate = new Date(quota?.last_reset_date)
        const nextResetDate = new Date(lastResetDate)
        nextResetDate.setDate(nextResetDate.getDate() + 1)
        return nextResetDate.toLocaleString()
    }
    return <div className="challenge-generator">
        <h2>Coding Challenge Generator</h2>

        <div className="quota-display">
            <p>Challenges remaining today: {quota?.quota_remaining || 0}</p>
            {quota?.quota_remaining === 0 && (
                <p> Next reset: {getNextResetTime()}</p>
            )}
        </div>
        <div className="difficulty-selector">
            <label htmlFor="difficulty">Select Difficulty</label>
            <select id="difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} disabled={isLoading}>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
        </div>
        <button onClick={generateChallenge} 
        disabled={false} 
        className="generate-button">
            {isLoading ? "Loading..." : "Generate Challenge"}
            </button>

        {error && <div className="error-message"><p>{error}</p></div>}
        {Challenge && <MCQChallenge Challenge={Challenge} />}
    </div>
}