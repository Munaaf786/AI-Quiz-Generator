from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import json
from datetime import datetime
from typing import List

from database import get_db, Quiz, create_db_tables
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz_from_text
from models import QuizGenerateRequest, QuizHistoryItem, FullQuizResponse, LLMFullQuizOutput as APILLMFullQuizOutput 


# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Ensuring database tables are created.")
    create_db_tables()
    yield  # The application starts and serves requests here
    print("Application shutdown: Resources can be cleaned up here.")

# Initialize FastAPI app with the lifespan
app = FastAPI(
    title="AI Wiki Quiz Generator API",
    description="API for generating quizzes from Wikipedia articles using LLMs.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware: Allows your frontend (running on a different port/origin)
origins = [
    "https://quizipedia-nine.vercel.app",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API ENDPOINTS ---

@app.post("/generate_quiz", response_model=FullQuizResponse, status_code=status.HTTP_201_CREATED)
async def generate_quiz(request: QuizGenerateRequest, db: Session = Depends(get_db)):
    """
    Generates a multiple-choice quiz from a given Wikipedia article URL.
    Scrapes the article, uses an LLM to create the quiz, and stores it in the database.
    """
    try:
        # 1. Scrape Wikipedia article
        scraped_data = scrape_wikipedia(str(request.url))
        article_title = scraped_data["title"]
        clean_text = scraped_data["clean_text"]
        raw_html = scraped_data["raw_html"]

        if not clean_text or len(clean_text) < 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scraped content is too short or empty. Cannot generate quiz."
            )

        # 2. Generate quiz using LLM
        # The LLM outputs data conforming to LLMFullQuizOutput schema
        raw_llm_output_dict = generate_quiz_from_text(article_title, clean_text)

        # Convert the dictionary output from LLM into our Pydantic model 
        llm_quiz_data = APILLMFullQuizOutput(**raw_llm_output_dict)

        # 3. Store in database
        # Serialize the LLM output (Pydantic object) to JSON string for storage
        db_quiz = Quiz(
            url=str(request.url), # Convert HttpUrl to string
            title=llm_quiz_data.title,
            scraped_content=raw_html, # Store raw HTML or clean text for bonus
            full_quiz_data=llm_quiz_data.model_dump_json(indent=2), # Convert Pydantic model to JSON string
            date_generated=datetime.now()
        )
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz) # Get the generated ID and other updated fields

        # 4. Prepare response
        # Deserialize the stored JSON back into the Pydantic model for response validation
        # and combine it with database specific fields
        response_data = APILLMFullQuizOutput.model_validate_json(db_quiz.full_quiz_data)
        return FullQuizResponse(
            id=db_quiz.id,
            url=db_quiz.url,
            title=db_quiz.title,
            summary=response_data.summary,
            key_entities=response_data.key_entities,
            sections=response_data.sections,
            quiz=response_data.quiz,
            related_topics=response_data.related_topics,
            date_generated=db_quiz.date_generated
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        # Catch errors from scraper or LLM generator
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")


@app.get("/history", response_model=List[QuizHistoryItem])
def get_quiz_history(db: Session = Depends(get_db)):
    """
    Retrieves a list of all previously generated quizzes (history).
    """
    quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
    # Map database objects to Pydantic response model
    return [
        QuizHistoryItem(
            id=quiz.id,
            url=quiz.url,
            title=quiz.title,
            date_generated=quiz.date_generated
        )
        for quiz in quizzes
    ]

@app.get("/quiz/{quiz_id}", response_model=FullQuizResponse)
def get_single_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the full details of a specific quiz by its ID.
    """
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    # Deserialize the stored JSON string back into the Pydantic model for response
    quiz_data_from_db = APILLMFullQuizOutput.model_validate_json(db_quiz.full_quiz_data)

    return FullQuizResponse(
        id=db_quiz.id,
        url=db_quiz.url,
        title=db_quiz.title,
        summary=quiz_data_from_db.summary,
        key_entities=quiz_data_from_db.key_entities,
        sections=quiz_data_from_db.sections,
        quiz=quiz_data_from_db.quiz,
        related_topics=quiz_data_from_db.related_topics,
        date_generated=db_quiz.date_generated
    )

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "AI Wiki Quiz Generator API is running!"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
