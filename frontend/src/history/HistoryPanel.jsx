import "react"
import { useState, useEffect } from "react"
import {MCQChallenge} from "../Challenge/MCQChallenge"
import { useApi } from "../utils/api"



export function HistoryPanel() {
    const [history, setHistory] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState(null)
    const {makeRequest} = useApi()
    useEffect(() => {
        fetchHistory()
    }, [])

    const fetchHistory = async() => {
        setIsLoading(true)
        setError(null)
        try {
            const response = await makeRequest("my-history")
            console.log('response history: ', response)
            setHistory(response?.challenges)
        } catch (error) {
            console.error("Error fetching history:", error)
            setError(error.message)
        } finally {
            setIsLoading(false)
        }
    }

    if(isLoading) {
        return <div className="loading">Loading History......</div>
    }

    if (error) {
        return <div className="error-message">
            <p>Error fetching history: {error}</p>
            <button onClick={fetchHistory}>retry</button>
        
        </div>
    }
    return <div className="history-panel">
        <h2>History</h2>
        {history?.length === 0 ? <p>No history found</p>  : <div className="history-list">

            {history.map((challenge) => 
            {
                return <MCQChallenge 
                key={challenge.id} 
                Challenge={challenge} 
                showExplanation={true}/>
            })
            }
            </div>
            }
    </div>
}