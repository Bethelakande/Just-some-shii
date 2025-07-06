import json
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from fastapi import HTTPException

def generate_challenge(difficulty,text):
    try:
        print("=================Debug Info staring AI generation=================")
        llm = ChatOllama(model="llama3.2", temperature=0.7)
        
        print("=========Template being created=========")
        
        # Create the prompt template with proper variable
        template = """You are an expert Questioner and challenge creator. 
Your task is to generate a question with multiple choice answers.
The question should be appropriate for the specified difficulty level: {difficulty}

This is some information from the text the user has provided; It is from the document the user has uploaded. Get your questoin from this piece of Information.
this is the text: {text}

Return the challenge in the following JSON structure:
{{
    "title": "The question (The question to be asked)",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer_id": 0,
    "explanation": "Detailed explanation of why the correct answer is right"
}}

Make sure the options are plausible but with only one clearly correct answer.
The response should be valid JSON ONLY, no additional text or formatting."""

        print("=========Template created=========")
        
        prompt = ChatPromptTemplate.from_template(template)
        
        print("=========Chain created=========")
        chain = prompt | llm
        
        print("=========Invoking chain=========")
        print("difficulty: ", difficulty)
        
        # Pass difficulty as a dictionary to the template
        response = chain.invoke({"difficulty": difficulty, "text": text})
        
        print("=========Chain invoked=========")
        print('response: ', response)
        print('clean response: ', response.content)
        
        # Parse the JSON response
        try:
            response_data = json.loads(response.content)
            print("=========JSON parsed=========")
            print("response_data: ", response_data)
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