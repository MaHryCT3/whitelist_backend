from pydantic import BaseModel


class ApproveApplicationPayload(BaseModel):
    approve_application_user_id: int


class DeclineApplicationPayload(BaseModel):
    decline_application_user_id: int
