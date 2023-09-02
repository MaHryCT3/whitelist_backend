from app.services.http import HTTPClient
from app.config import settings


class TelegramService(HTTPClient):
    API_TOKEN = settings.TELEGRAM_TOKEN

    BASE_URL = f'https://api.telegram.org/bot{API_TOKEN}/'

    async def send_message(self, chat_id: int, message: str) -> None:
        await self.request(
            f'sendMessage',
            'GET',
            query={'chat_id': chat_id, 'text': message},
        )