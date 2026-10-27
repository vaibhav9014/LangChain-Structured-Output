LangChain Structured Output
A beginner-friendly learning project for understanding structured output in LangChain.

In LangChain, structured output means asking a language model to return its response in a well-defined data format—such as JSON or a Pydantic object—instead of free-form text. This makes the model output easier to parse, validate, and use programmatically.

This project starts from a simple Pydantic schema and moves toward using that schema with a LangChain chat model.

Table of Contents
Project Goal

What Is Structured Output?

Why Do We Need Structured Output?

Ways to Define Structured Output

TypedDict

Pydantic

JSON Schema

When to Use What

Output Parsers

Types of Output Parsers

Project Structure

Code Explanation

How to Run

Environment Variables

Example Output

Common Errors

Current Status

Next Steps

Project Goal
The goal of this project is to learn how to make a language model return predictable, structured data.

Instead of receiving a paragraph like this:

text
The student is Riya Sharma. Her email is riya@example.com and her CGPA is 8.7.
we want the model to return structured data like this:

python
Student(
    name="Riya Sharma",
    email="riya@example.com",
    cgpa=8.7
)
This project explains:

What structured output is.

Why applications need it.

How to define an output structure.

How to use Pydantic for validation.

How to connect a schema to a LangChain model.

How output parsers work.

What Is Structured Output?
Structured output is the practice of having a language model return a response in a well-defined data format, such as JSON, rather than free-form text.

For example, instead of asking a model to “extract student details” and receiving a sentence, we define a schema:

python
class Student(BaseModel):
    name: str
    email: EmailStr
    cgpa: float
Now the model is guided to return:

json
{
  "name": "Riya Sharma",
  "email": "riya@example.com",
  "cgpa": 8.7
}
This makes the output easier to parse and work with programmatically.

Why Do We Need Structured Output?
Structured output is useful in three common situations.

1. Data Extraction
You can extract useful information from unstructured text.

Example:

text
Input:
Riya Sharma can be contacted at riya@example.com. She scored 8.7 CGPA.

Output:
{
  "name": "Riya Sharma",
  "email": "riya@example.com",
  "cgpa": 8.7
}
2. API Building
APIs usually need predictable data.

If your API expects a student’s name, email, and CGPA, the model response must match that structure. Structured output helps ensure the response can be safely used by the API.

3. Agents
Agents often need to decide what action to take.

For example, an agent may need to return:

json
{
  "action": "search_web",
  "query": "latest LangChain version"
}
Structured output makes it easier for the application to understand the agent’s decision and execute the correct tool.

Ways to Define Structured Output
There are three common ways to define structured output:

TypedDict

Pydantic

JSON Schema

TypedDict
TypedDict is a way to define the expected keys and value types of a dictionary in Python.

Example:

python
from typing import TypedDict

class Student(TypedDict):
    name: str
    email: str
    cgpa: float
This tells Python that a Student dictionary should contain:

name, which should be a string.

email, which should be a string.

cgpa, which should be a float.

Why use TypedDict?
TypedDict helps with:

Code readability.

Editor autocomplete.

Type hints.

Defining the expected dictionary structure.

Important limitation
TypedDict does not validate data at runtime.

For example, this will not automatically raise an error:

python
student: Student = {
    "name": 123,
    "email": "not-an-email",
    "cgpa": "high"
}
Python will not stop you here. TypedDict is mainly a hint for developers and tools; it does not enforce correctness by itself.

Pydantic
Pydantic is a data validation and data parsing library for Python.

It ensures that the data you work with is correct, structured, and type-safe.

Example:

python
from pydantic import BaseModel, Field, EmailStr

class Student(BaseModel):
    name: str = Field(description="Student's full name")
    email: EmailStr = Field(description="Student's email address")
    cgpa: float = Field(
        gt=0,
        lt=10,
        default=5,
        description="A decimal value representing the CGPA of the student"
    )
Unlike TypedDict, Pydantic validates data at runtime.

For example:

python
Student(name="Riya", email="riya@example.com", cgpa=8.7)
This is valid.

But this:

python
Student(name="Riya", email="invalid-email", cgpa=20)
will raise a validation error because:

The email is invalid.

cgpa is not less than 10.

Why use Pydantic?
Use Pydantic when:

You need data validation.

You need automatic type conversion.

You need default values.

You need constraints such as “CGPA must be between 0 and 10.”

You want to trust the final data before using it in your application.

You are building APIs, agents, or data-extraction pipelines.

JSON Schema
JSON Schema is a standard way to describe the structure of JSON data.

Example:

json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "cgpa": {
      "type": "number"
    }
  },
  "required": ["name", "email", "cgpa"]
}
Why use JSON Schema?
Use JSON Schema when:

You want a language-independent structure.

You want to define the schema in standard JSON format.

You do not need a Python object.

You want to pass the schema directly to a model or API.

You want to validate JSON data.

When to Use What
Approach	Best for	Runtime validation	Python object	Example use case
TypedDict	Type hints and editor support	No	Dictionary	Simple internal Python structures
Pydantic	Validation, parsing, defaults, constraints	Yes	Pydantic model	APIs, data extraction, agents
JSON Schema	Standard, language-independent schema	Depends on validator	No	Model APIs and external integrations
Simple rule
Use TypedDict when you only need type hints.

Use Pydantic when you need validation.

Use JSON Schema when you need a standard JSON structure.

Output Parsers
An output parser in LangChain converts raw LLM responses into a structured format, such as JSON, CSV, Pydantic models, and more.

Output parsers help ensure:

Consistency.

Validation.

Easier access to individual fields.

Better integration with application logic.

Without a parser:

python
response.content
returns text.

With a parser:

python
parsed_result.name
parsed_result.email
parsed_result.cgpa
returns individual fields.

Types of Output Parsers
LangChain provides several output parsers.

1. String Output Parser
Returns the model response as a plain string.

python
from langchain_core.output_parsers import StrOutputParser
Use this when you only need text.

2. JSON Output Parser
Parses a JSON-formatted model response into a Python dictionary.

python
from langchain_core.output_parsers import JsonOutputParser
Use this when you want JSON data but do not need Pydantic validation.

3. Pydantic Output Parser
Parses model output into a Pydantic model.

python
from langchain_core.output_parsers import PydanticOutputParser
Use this when you need validation and typed Python objects.

4. Comma-Separated List Output Parser
Converts a comma-separated response into a Python list.

python
from langchain_core.output_parsers import CommaSeparatedListOutputParser
Example:

text
apple, banana, mango
becomes:

python
["apple", "banana", "mango"]
5. Structured Output Parser
Converts output into a dictionary based on a defined schema.

This is useful for simple structured responses without full Pydantic validation.

Project Structure
text
Structure Output/
├── .env
├── .gitignore
├── README.md
├── pydantic_demo.py
├── structured_output_demo.py
└── venv/
pydantic_demo.py
Demonstrates how to define and validate a Pydantic schema.

structured_output_demo.py
Demonstrates how to connect a Pydantic schema to a LangChain chat model using with_structured_output().

.env
Stores the API key.

venv/
Contains the virtual environment. This should not be committed to GitHub.

Code Explanation
pydantic_demo.py
python
from pydantic import BaseModel, Field, EmailStr
This imports the tools needed to define and validate the schema.

BaseModel is used to create a Pydantic model.

Field is used to add descriptions, defaults, and validation rules.

EmailStr is used to validate email addresses.

python
class Student(BaseModel):
This creates a Pydantic model named Student.

python
    name: str = Field(description="Student's full name")
This defines a field called name.

It must be a string.

The description tells the model what this field means.

python
    email: EmailStr = Field(description="Student's email address")
This defines an email field.

EmailStr validates that the value is a valid email address.

The description guides the model.

python
    cgpa: float = Field(
        gt=0,
        lt=10,
        default=5,
        description="A decimal value representing the CGPA of the student"
    )
This defines the CGPA field.

It must be a float.

It must be greater than 0.

It must be less than 10.

If the model does not provide it, the default value is 5.

python
student = Student(
    name="Riya Sharma",
    email="riya@example.com",
    cgpa=8.7
)
This creates a validated Student object.

python
print(student)
This prints the complete validated object.

python
print(student.name)
print(student.email)
print(student.cgpa)
These lines access individual fields from the object.

structured_output_demo.py
python
from pydantic import BaseModel, Field, EmailStr
This imports Pydantic tools for defining the output schema.

python
from langchain_openai import ChatOpenAI
This imports LangChain’s OpenAI chat model class.

python
class Student(BaseModel):
    name: str = Field(description="Student's full name")
    email: EmailStr = Field(description="Student's email address")
    cgpa: float = Field(
        gt=0,
        lt=10,
        default=5,
        description="A decimal value representing the CGPA of the student"
    )
This defines the structure that the model should return.

python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
This creates the chat model.

model="gpt-4o-mini" selects the model.

temperature=0 makes the output more deterministic and consistent.

python
structured_llm = llm.with_structured_output(Student)
This is the most important line.

It tells LangChain:

“When this model responds, format and validate the response using the Student schema.”

python
result = structured_llm.invoke(
    "Extract the student details: Riya Sharma, riya@example.com, CGPA 8.7"
)
This sends the prompt to the model.

The model is expected to return data matching the Student schema.

python
print(result)
This prints the parsed and validated Pydantic object.

python
print(result.name)
print(result.email)
print(result.cgpa)
These lines access the extracted fields directly.

How to Run
1. Activate the virtual environment
macOS and Linux:

bash
source venv/bin/activate
Windows PowerShell:

powershell
venv\Scripts\Activate.ps1
2. Install dependencies
bash
pip install langchain langchain-core langchain-openai "pydantic[email]" python-dotenv
3. Set the API key
For the current terminal session:

bash
export OPENAI_API_KEY="your_api_key"
4. Run the Pydantic demo
bash
python pydantic_demo.py
5. Run structured output with LangChain
bash
python structured_output_demo.py
Environment Variables
Variable	Description
OPENAI_API_KEY	API key used to access OpenAI models
Create a .env file:

text
OPENAI_API_KEY=your_openai_api_key
Never commit .env or an API key to GitHub.

Add this to .gitignore:

text
.env
venv/
.venv/
__pycache__/
Example Output
Pydantic demo
python
Student(
    name="Riya Sharma",
    email="riya@example.com",
    cgpa=8.7
)
Structured output demo
python
name="Riya Sharma"
email="riya@example.com"
cgpa=8.7
The exact formatting may vary, but the important point is that the response becomes structured and validated data.

Common Errors
email-validator is not installed
text
ImportError: email-validator is not installed
This happens when you use EmailStr without installing the email validation package.

Fix:

bash
pip install "pydantic[email]"
Missing credentials
text
OpenAIError: Missing credentials
This means OPENAI_API_KEY is not set.

Fix:

bash
export OPENAI_API_KEY="your_api_key"
Wrong activation command on macOS
This is a Windows command:

bash
venv\Scripts\activate
On macOS or Linux, use:

bash
source venv/bin/activate
Current Status
Completed:

Pydantic schema creation.

Field descriptions.

Email validation.

Numeric validation.

Default values.

OpenAI model invocation.

Structured output using with_structured_output().

Accessing parsed fields.

Next Steps
Add JSON output parser examples.

Add TypedDict structured output examples.

Add JSON Schema examples.

Add error handling for invalid model responses.

Add retry logic when parsing fails.

Add multiple schemas for different tasks.

Add nested Pydantic models.

Add list-based output schemas.

Add tests for schemas and parsers.

Build a small API using FastAPI.