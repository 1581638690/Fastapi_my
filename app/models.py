from database import Base
from sqlalchemy import Column, INT, String, BOOLEAN, Integer, DateTime, TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(BOOLEAN, default=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default=text('now()'))

    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default=text('now()'))


class Votes(Base):
    __tablename__ = "votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete='CASCADE'),nullable=False,primary_key=True)

