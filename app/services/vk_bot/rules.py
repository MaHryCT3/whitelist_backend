from pydantic import BaseModel
from vkbottle.bot import rules


class PydanticPayloadRule(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, payload_model: type[BaseModel]):
        self.payload_model = payload_model

    async def check(self, event: rules.BaseMessageMin) -> bool | dict[str, BaseModel]:
        payload = event.get_payload_json()
        if not payload.keys() == self.payload_model.__fields__.keys():
            return False
        return {'payload': self.payload_model(**payload)}
