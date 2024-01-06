from sqlmodel import Session, SQLModel, create_engine, select

from models import Flashcard, Tag

engine = create_engine("sqlite:///flashy.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


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


def get_flashcards():
    """Get all flashcards from the database."""
    with Session(engine) as session:
        cards = session.exec(select(Flashcard)).all()

        for card in cards:
            print(card)
            print(card.tags)


def main():
    create_db_and_tables()
    add_flashcard("Tell me about yourself.", "I'm a software developer.", "Interview")
    get_flashcards()


if __name__ == "__main__":
    main()
