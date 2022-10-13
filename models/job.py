from pydantic import BaseModel


class Job(BaseModel):
    lang: str
    site: str
    title: str
    testing: bool = False
