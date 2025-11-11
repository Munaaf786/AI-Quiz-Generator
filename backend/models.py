from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
import datetime

# Pydantic schema for a single quiz question
class QuizQuestion(BaseModel):
    question: str = Field(..., description="The quiz question text.")
    options: List[str] = Field(..., description="Four possible answer options (A, B, C, D).")
    answer: str = Field(..., description="The correct answer among the options.")
    difficulty: str = Field(..., description="Difficulty level: 'easy', 'medium', or 'hard'.")
    explanation: str = Field(..., description="A short explanation for the answer.")


# Pydantic schema for the LLM's full output
class LLMFullQuizOutput(BaseModel):
    title: str = Field(..., description="The title of the Wikipedia article.")
    summary: str = Field(..., description="A short summary of the Wikipedia article.")
    key_entities: Dict[str, List[str]] = Field(..., description="Key entities categorized (e.g., people, organizations, locations).")
    sections: List[str] = Field(..., description="Main sections of the Wikipedia article.")
    quiz: List[QuizQuestion] = Field(..., description="A list of 5-10 quiz questions.")
    related_topics: List[str] = Field(..., description="Suggested related Wikipedia topics for further reading.")

# Pydantic schema for the API request body when generating a quiz
class QuizGenerateRequest(BaseModel):
    url: HttpUrl = Field(..., description="The Wikipedia article URL to generate a quiz from.")

# Pydantic schema for a simplified quiz history entry
class QuizHistoryItem(BaseModel):
    id: int
    url: str
    title: str
    date_generated: datetime.datetime

# Pydantic schema for the full quiz response from the API, combining LLM output with DB metadata
class FullQuizResponse(BaseModel):
    id: int
    url: HttpUrl
    title: str
    summary: str
    key_entities: Dict[str, List[str]]
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]
    date_generated: datetime.datetime