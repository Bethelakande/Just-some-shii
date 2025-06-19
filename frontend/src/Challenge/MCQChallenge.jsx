import "react"
import { useState } from "react"
export function MCQChallenge({Challenge, showExplanation = false}) {
    const [selectedOption, setSelectedOption] = useState(null)
    const [shouldShowExplanation, setShouldShowExplanation] = useState(showExplanation)

    const options = typeof Challenge.options === "string" ? JSON.parse(Challenge.options) : Challenge.options


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
                <div className={getOptionClass(index)} key={index} onClick={() => handleOptionSelect(index)}>{option}</div>
            ))}
        </div>
        {shouldShowExplanation && selectedOption !== null && (
            <div className="explanation">
                <h4>Explanation</h4>
                <p>{Challenge.explanation}</p>
            </div>
        )}
    </div>
}