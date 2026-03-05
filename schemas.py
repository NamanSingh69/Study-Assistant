from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Any, Dict

class GenerateQuizzesRequest(BaseModel):
    notes: Optional[str] = None
    original_text: Optional[str] = None
    existing_questions: str = "[]"
    question_types: List[str] = ["MCQ"]
    num_questions: int = Field(default=5, ge=1, le=50)
    difficulty: str = Field(default="Apply")

class GenerateFlashcardsRequest(BaseModel):
    notes: Optional[str] = None
    original_text: Optional[str] = None
    existing_flashcards: str = "[]"
    num_flashcards: int = Field(default=10, ge=1, le=100)

class GenerateMindmapRequest(BaseModel):
    notes: Optional[str] = None
    original_text: Optional[str] = None

class ChatRequest(BaseModel):
    notes: Optional[str] = None
    original_text: Optional[str] = None
    history: List[Dict[str, Any]] = []
    message: str
    web_search_enabled: bool = False

class EvaluateAnswerRequest(BaseModel):
    question: str
    ideal_answer: str
    user_answer: str
    notes_context: str
