from sqlalchemy import Column, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class StartRecord(Base):
    __tablename__ = "start_record"

    id = Column(
        BigInteger,
        primary_key=True
    )
    connection_id = Column(
        String(255),
        nullable=False,
    )
    timestamp = Column(
        BigInteger,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"StartRecord(id={self.id}, start_time={self.consume_time})"


if __name__ == "__main__":
    from database import engine
    Base.metadata.create_all(engine)
