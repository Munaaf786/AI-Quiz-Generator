import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

# Pydantic schema for the quiz output, mirroring the *exact* sample API structure
# This schema is used by LangChain's JsonOutputParser
class LLMQuizQuestion(BaseModel):
    question: str = Field(description="The quiz question text.")
    options: List[str] = Field(description="Four possible answer options (A, B, C, D).")
    answer: str = Field(description="The correct answer among the options.")
    difficulty: str = Field(description="Difficulty level: 'easy', 'medium', or 'hard' (lowercase).")
    explanation: str = Field(description="A short explanation for the answer.")

class LLMFullQuizOutput(BaseModel):
    title: str = Field(description="The title of the Wikipedia article.")
    summary: str = Field(description="A short summary of the Wikipedia article, max 3 sentences.")
    key_entities: Dict[str, List[str]] = Field(description="A dictionary of key entities categorized, e.g., {'people': ['Alice'], 'organizations': ['OrgX'], 'locations': ['PlaceY']}. Include 'people', 'organizations', and 'locations'.")
    sections: List[str] = Field(description="A list of 3-5 main sections or subheadings from the Wikipedia article.")
    quiz: List[LLMQuizQuestion] = Field(description="A list of exactly 5 multiple-choice quiz questions.")
    related_topics: List[str] = Field(description="A list of 3-5 suggested related Wikipedia topics for further reading.")

# Initialize the Gemini LLM
# Using gemini-pro for text generation tasks
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=GEMINI_API_KEY, temperature=0.7)

# Define the output parser based on our Pydantic schema
parser = JsonOutputParser(pydantic_object=LLMFullQuizOutput)

# Define the prompt template
# This prompt provides detailed instructions to the LLM on content and strict JSON formatting.
prompt_template = PromptTemplate(
    template="""
    You are an expert quiz generator. Your task is to analyze the provided Wikipedia article content
    and generate a structured JSON output strictly following the specified schema.

    Here are the formatting instructions:
    {format_instructions}

    Article Title: {article_title}
    Article Content:
    {article_content}

    ---
    **Instructions for Generation:**
    1.  **Summary:** Provide a concise summary of the article, maximum 3 sentences.
    2.  **Key Entities:** Identify 3-5 key entities and categorize them into 'people', 'organizations', and 'locations' as a dictionary.
    3.  **Sections:** List 3-5 main section titles or important subheadings from the article.
    4.  **Quiz:** Generate exactly 5 multiple-choice questions. Each question must have 4 options (A, B, C, D), a correct answer (which must be one of the options), an explanation, and a difficulty level ('easy', 'medium', or 'hard').
    5.  **Related Topics:** Suggest 3-5 relevant Wikipedia topics for further reading.

    Ensure your output is valid JSON and strictly adheres to the schema.
    """,
    input_variables=["article_title", "article_content"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Create the LangChain sequence (chain): Prompt -> LLM -> Parser
quiz_generation_chain: RunnableSequence = prompt_template | llm | parser

def generate_quiz_from_text(title: str, text_content: str) -> Dict:
    """
    Generates a structured quiz using the LLM based on provided article title and content.
    """
    try:
        # Invoke the chain to get the structured quiz output
        quiz_data = quiz_generation_chain.invoke(
            {"article_title": title, "article_content": text_content}
        )
        return quiz_data
    except Exception as e:
        raise RuntimeError(f"Error generating quiz with LLM: {e}")

# Example usage (for testing)
if __name__ == "__main__":
    print("Testing LLM quiz generation with updated schema (this might take a moment)...")
    sample_title = "Alan Turing"
    sample_content = """
    Alan Mathison Turing OBE FRS (23 June 1912 – 7 June 1954) was a British mathematician, computer scientist,
    logician, cryptanalyst, philosopher, and theoretical biologist. He was highly influential in the development
    of theoretical computer science, providing a formalisation of the concepts of algorithm and computation with
    the Turing machine, which can be considered a model of a general-purpose computer. Turing is widely considered
    to be the father of theoretical computer science and artificial intelligence.

    During the Second World War, Turing worked for the Government Code and Cypher School (GC&CS) at Bletchley Park,
    Britain's codebreaking centre. For a time, he led Hut 8, the section responsible for German naval cryptanalysis.
    He devised a number of techniques for speeding up the breaking of German ciphers, including improvements to the
    pre-war Polish bombe method, and contributed to the design of the British Bombe, an electromechanical machine
    used to help decipher Enigma signals.
    """
    try:
        generated_quiz = generate_quiz_from_text(sample_title, sample_content)
        print("\n--- Generated Quiz Sample (matching API structure) ---")
        import json
        print(json.dumps(generated_quiz, indent=2))
    except RuntimeError as e:
        print(f"Test failed: {e}")