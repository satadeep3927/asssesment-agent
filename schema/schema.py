import json
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class BloomsTaxonomyLevel(str, Enum):
    """Bloom's Taxonomy cognitive levels"""

    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class DifficultyLevel(str, Enum):
    """Question difficulty levels"""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"


class QuestionType(str, Enum):
    """Types of assessment questions"""

    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"


class MCQOption(BaseModel):
    """Multiple choice question option"""

    option_id: str = Field(..., description="Option identifier (A, B, C, D)")
    text: str = Field(..., description="Option text content")
    is_correct: bool = Field(False, description="Whether this is the correct answer")


class AnswerKey(BaseModel):
    """Answer key for different question types"""

    correct_answer: Optional[Union[str, List[str]]] = Field(
        None, description="Correct answer(s)"
    )
    explanation: Optional[str] = Field(
        None, description="Explanation of the correct answer"
    )
    marking_criteria: Optional[str] = Field(
        None, description="Detailed marking rubric for long answers"
    )
    key_points: Optional[List[str]] = Field(
        None, description="Key points to award marks"
    )


class Question(BaseModel):
    """Individual assessment question"""

    question_type: QuestionType = Field(..., description="Type of question")
    question_text: str = Field(..., description="The actual question content")
    marks: int = Field(..., description="Marks allocated to this question", ge=1)
    blooms_level: BloomsTaxonomyLevel = Field(..., description="Bloom's taxonomy level")
    difficulty: DifficultyLevel = Field(..., description="Question difficulty level")

    # For MCQ questions
    options: Optional[List[MCQOption]] = Field(
        None, description="Multiple choice options"
    )

    # Answer information
    answer_key: AnswerKey = Field(..., description="Answer key and marking guide")

    # Additional metadata
    learning_objective_covered: Optional[str] = Field(
        None, description="Specific learning objective addressed"
    )
    estimated_time_minutes: Optional[int] = Field(
        None, description="Estimated time to complete"
    )


class AssessmentMetadata(BaseModel):
    """Metadata about the generated assessment"""

    total_questions: int = Field(..., description="Total number of questions generated")
    total_marks: int = Field(..., description="Total marks for the assessment")
    estimated_duration_minutes: Optional[int] = Field(
        None, description="Estimated completion time"
    )
    difficulty_distribution: dict = Field(
        ..., description="Distribution of questions by difficulty"
    )
    question_type_distribution: dict = Field(
        ..., description="Distribution by question type"
    )
    blooms_level_coverage: dict = Field(
        ..., description="Coverage of Bloom's taxonomy levels"
    )


class AssessmentResult(BaseModel):
    """Complete assessment result model"""

    title: str = Field(..., description="Assessment title")
    description: Optional[str] = Field(None, description="Assessment description")

    # Assessment parameters
    curriculum_standard: str = Field(..., description="Curriculum standard assessed")
    learning_objectives: str = Field(..., description="Learning objectives covered")
    target_blooms_level: BloomsTaxonomyLevel = Field(
        ..., description="Primary Bloom's taxonomy level"
    )

    # Questions and answers
    questions: List[Question] = Field(..., description="List of assessment questions")

    # Metadata
    metadata: AssessmentMetadata = Field(
        ..., description="Assessment metadata and statistics"
    )

    # Instructions
    student_instructions: str = Field(
        ..., description="Instructions for students taking the assessment"
    )
    teacher_notes: Optional[str] = Field(
        None, description="Additional notes for teachers"
    )


class AssessmentRequest(BaseModel):
    """Request model for generating assessments"""

    curriculum_standard: str = Field(
        ..., description="The curriculum standard to assess"
    )
    learning_objectives: str = Field(..., description="Specific learning objectives")
    blooms_taxonomy_level: BloomsTaxonomyLevel = Field(
        ..., description="Target Bloom's taxonomy level"
    )
    toughness_level: DifficultyLevel = Field(
        ..., description="Overall difficulty level"
    )
    total_marks: int = Field(..., description="Total marks for the assessment", ge=1)
    number_of_questions: int = Field(
        ..., description="Number of questions to generate", ge=1
    )
    additional_prompts: Optional[str] = Field(
        None, description="Additional requirements or constraints"
    )

    # Question distribution preferences
    mcq_percentage: Optional[float] = Field(
        0.4, description="Percentage of MCQ questions", ge=0, le=1
    )
    short_answer_percentage: Optional[float] = Field(
        0.3, description="Percentage of short answer questions", ge=0, le=1
    )
    long_answer_percentage: Optional[float] = Field(
        0.3, description="Percentage of long answer questions", ge=0, le=1
    )

    response_format: Optional[str] = Field(
        json.dumps(AssessmentResult.model_json_schema()),
        description="Format of the response",
    )
