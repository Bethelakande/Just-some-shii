import json
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from fastapi import HTTPException

def generate_challenge(difficulty):
    try:
        print("=================Debug Info staring AI generation=================")
        llm = ChatOllama(model="llama3.2", temperature=0.7)
        
        print("=========Template being created=========")
        
        # Create the prompt template with proper variable
        template = """You are an expert coding challenge creator. 
Your task is to generate a coding question with multiple choice answers.
The question should be appropriate for the specified difficulty level: {difficulty}

For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

Return the challenge in the following JSON structure:
{{
    "title": "The question title",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer_id": 0,
    "explanation": "Detailed explanation of why the correct answer is right"
}}

Make sure the options are plausible but with only one clearly correct answer.
The response should be valid JSON only, no additional text or formatting."""

        print("=========Template created=========")
        
        prompt = ChatPromptTemplate.from_template(template)
        
        print("=========Chain created=========")
        chain = prompt | llm
        
        print("=========Invoking chain=========")
        print("difficulty: ", difficulty)
        
        # Pass difficulty as a dictionary to the template
        response = chain.invoke({"difficulty": difficulty})
        
        print("=========Chain invoked=========")
        print('response: ', response)
        print('clean response: ', response.content)
        
        # Parse the JSON response
        try:
            response_data = json.loads(response.content)
        except json.JSONDecodeError as json_error:
            print(f"JSON parsing error: {json_error}")
            print(f"Raw response: {response.content}")
            raise ValueError(f"Invalid JSON response from AI: {json_error}")
        
        # Validate required fields
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in response_data:
                raise ValueError(f"Missing required field: {field}")
        
        print("=========Response validated=========")
        print(f"Returning response in format: {response_data}")
        
        return response_data
        
    except Exception as e:
        print("=========Exception occurred=========")
        print("Exception: ", e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")