import typer
import time

from typing import Optional
from rich import print

from sqlmodel import Session, SQLModel, create_engine, select
from models import Flashcard, Tag, FlashcardTagLink

# Create the Typer object to define the CLI
app = typer.Typer()

# Create the database engine
engine = create_engine("sqlite:///flashy.db")


def create_db_and_tables():
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


@app.command()
def add_flashcard(question, answer, tags=None):
    """Add a flashcard to the database."""
    if tags is None:
        tags = []
    else:
        tags = tags.split(", ")

    with Session(engine) as session:
        # Fetch all existing tags in one query
        existing_tags = session.exec(select(Tag).where(Tag.name.in_(tags))).all()
        existing_tags_dict = {tag.name: tag for tag in existing_tags}

        tag_list = []
        for tag in tags:
            if tag not in existing_tags_dict:
                # Tag doesn't exist, so create it and add it to the list
                new_tag = Tag(name=tag)
                tag_list.append(new_tag)
                existing_tags_dict[tag] = new_tag
            else:
                # Tag exists so get it from the dictionary and add it to the list
                tag_list.append(existing_tags_dict[tag])

        # Create the flashcard
        card = Flashcard(question=question, answer=answer, tags=tag_list)
        session.add(card)
        session.commit()


@app.command()
def get_flashcards(tag: Optional[str] = None):
    """Get all flashcards from the database."""

    welcome()

    with Session(engine) as session:
        if tag is None:
            flashcards = session.exec(select(Flashcard)).all()
        else:
            flashcards = session.exec(
                select(Flashcard)
                .join(FlashcardTagLink)
                .join(Tag)
                .where(Tag.name == tag)
            ).all()

        for card in flashcards:
            qa_console(card)


def welcome():
    """Welcome the user."""
    print("Welcome to Flashy!")
    print("Press Ctrl+C to exit.")
    print("----------------------------------")
    print("")


def qa_console(card):
    """Ask and answer a flashcard."""
    print(f"[bold red]Question:[/bold red] [white]{card.question}[/white]")
    time.sleep(2)
    typer.prompt("Rate the difficulty of this question (1-5)")
    print(f"[bold green]Answer:[/bold green] [white]{card.answer}[/white]")
    print("----------------------------------")


if __name__ == "__main__":
    app()
