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


class CommandRule(rules.ABCRule[rules.BaseMessageMin]):
    def __init__(self, command_text: str, prefix: str = '/'):
        self.command_text = command_text
        self.prefix = prefix

    async def check(self, event: rules.BaseMessageMin) -> dict | bool:
        no_prefix = event.text.removeprefix('/')
        if no_prefix.startswith(self.command_text):
            no_command = no_prefix.removeprefix(self.command_text + ' ')
            return {'args': no_command}
        else:
            return False

