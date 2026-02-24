from sqlalchemy import Column, Integer, String, Boolean


class ToDO():
    __tablename__ = "Todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)
