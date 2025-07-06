import {useAuth} from "@clerk/clerk-react"

export const useApi = () => {
    const {getToken} = useAuth()

    const makeRequest = async (endpoint, Options = {}) => {
        const token = await getToken()

        const defaultOptions = {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            }
        }

        if (Options.body instanceof FormData) {
            delete defaultOptions.headers["Content-Type"]
        }

        console.log('Options: ', Options)
        console.log('defaultOptions: ', defaultOptions)

        const response = await fetch(`http://localhost:8001/api/${endpoint}`,{
            ...defaultOptions,
            ...Options
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => null)
            if (response.status === 429){
                throw new Error ("Dailt Quota Exceeded")
            }
            if (response.status === 401){
                throw new Error ("Unauthorized")
            }
            if (response.status === 403){
                throw new Error ("Forbidden")
            }
            throw new Error (errorData?.detail || "Network response was not ok")
        }

        return response.json()
    }
    return {
        makeRequest
    }
}
