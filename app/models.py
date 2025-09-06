import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import UniqueConstraint, Index
from app import db

class Bible(db.Model):
    __tablename__ = "bible_search_bible"
    id:so.Mapped[int] = so.mapped_column(primary_key=True)
    book_code: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, nullable=False)
    book:so.Mapped[str] = so.mapped_column(sa.String(50), index=True, nullable=False)
    chapter:so.Mapped[int] = so.mapped_column(sa.Integer(), index=True, nullable=False)
    verse:so.Mapped[int] = so.mapped_column(sa.Integer(), index=True, nullable=False)
    text:so.Mapped[str] = so.mapped_column(sa.String())
    translation:so.Mapped[str] = so.mapped_column(sa.String(20), index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("book", "chapter", "verse", "text", "translation", "book_code",
                         name="uq_bible_translation_loc"),
        Index("ix_bible_loc", "book_code", "chapter", "verse")
    )

    def __repr__(self):
        return f"<{self.book_code} - {self.book}>"

    def to_dict(self):
        return {
            "id": self.id,
            "book": self.book,
            "chapter": self.chapter,
            "verse": self.verse,
            "text": self.text,
            "translation": self.translation,
            "book_code": self.book_code
        }