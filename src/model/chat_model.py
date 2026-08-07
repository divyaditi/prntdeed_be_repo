from pydantic import BaseModel, Field, validator

class ChatModel(BaseModel):
    message:str = Field(..., description="The chat message from the user")

    @validator('message')
    def validate_message(cls, value):
        if not value or not value.strip():
            raise ValueError("Chat message cannot be empty.")
        return value