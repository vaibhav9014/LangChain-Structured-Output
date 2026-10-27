from pydantic import BaseModel, Field, EmailStr
from langchain_openai import ChatOpenAI

class Student(BaseModel):
    name: str = Field(description="Student's full name")
    email: EmailStr = Field(description="Student's email address")
    cgpa: float = Field(
        gt=0,
        lt=10,
        default=5,
        description="A decimal value representing the CGPA of the student",
    )

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

structured_llm = llm.with_structured_output(Student)

result = structured_llm.invoke(
    "Extract the student details: Riya Sharma, riya@example.com, CGPA 8.7"
)

print(result)
print(result.name)
print(result.email)
print(result.cgpa)
