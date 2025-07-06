import "react"
import { useEffect, useState } from "react"
export function MCQChallenge({Challenge, showExplanation = false}) {
    const [selectedOption, setSelectedOption] = useState(null)
    const [shouldShowExplanation, setShouldShowExplanation] = useState(showExplanation)



    useEffect(() => {
        // Reset selected option and explanation when Challenge changes
        setSelectedOption(null)
        setShouldShowExplanation(showExplanation)
    }, [Challenge, showExplanation])

    console.log('Challenge: ', Challenge)
    const options = typeof Challenge.options === "string" 
        ? JSON.parse(Challenge.options)
        : Array.isArray(Challenge.options) 
            ? Challenge.options.map(option => typeof option === 'object' ? option.value || option.description : option)
            : [Challenge.options];

    console.log('options: ', options)

    const handleOptionSelect = (index) => {
        if (selectedOption !== null) return
        setSelectedOption(index)
        setShouldShowExplanation(true)
    }
    

    const getOptionClass = (index) => {
        if (selectedOption === null) return "option"

        if (index === Challenge.correct_answer_id) {
            return "option correct"
        }
        if (selectedOption === index && index !== Challenge.correct_answer_id) {
            return "option incorrect"
        }

        return "option"
    }
    return <div className="challenge-display">
        <p><strong>Difficulty</strong>: {Challenge.difficulty}</p>
        <p className="challenge-title">{Challenge.title}</p>
        <div className="options">
            {options.map((option, index) => (
                <div className={getOptionClass(index)} key={index} onClick={() => handleOptionSelect(index)}>
                    {typeof option === 'object' ? option.value || option.description : option}
                </div>
            ))}
        </div>
        {shouldShowExplanation && (
            <div className="explanation">
                <h3>Explanation:</h3>
                <p>{Challenge.explanation}</p>
            </div>
        )}
    </div>
}