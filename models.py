from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class FlashcardTagLink(SQLModel, table=True):
    flashcard_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="flashcard.id"
    )
    tag_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="tag.id")


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    flashcards: List["Flashcard"] = Relationship(
        back_populates="tags", link_model=FlashcardTagLink
    )


class Flashcard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    answer: str
    tags: List[Tag] = Relationship(
        back_populates="flashcards", link_model=FlashcardTagLink
    )
    difficulty: int = 1  # 1-5
