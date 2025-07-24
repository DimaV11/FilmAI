from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import logging

logging.basicConfig(filename='gigachat.log', level=logging.DEBUG)

class GigaChatAPI:
    def __init__(self, client_secret: str, model: str = "GigaChat"):
        self.client_secret = client_secret
        self.model = model
        logging.debug(f"Инициализация GigaChat с credentials={client_secret[:10]}... и model={model}")
        try:
            self.client = GigaChat(
                credentials=self.client_secret,
                model=self.model,
                verify_ssl_certs=False
            )
        except Exception as e:
            logging.error(f"Ошибка инициализации GigaChat: {str(e)}")
            raise

    def get_films(self, prompt: str) -> str:
        """Запрос к GigaChat для получения рекомендаций фильмов"""
        try:
            chat = Chat(
                messages=[
                    Messages(
                        role=MessagesRole.SYSTEM,
                        content=(
                            "Ты - эксперт по фильмам и сериалам. "
                            "Пользователь описывает сюжет, тематику или настроение, "
                            "ты рекомендуешь 3-5 фильмов или сериалов с кратким описанием и рейтингом в Кинопоиск или IMDB (НИЧЕГО ДРУГОГО, ТОЛЬКО ДВА РЕЙТИНГА КИНОПОИСК И IMDB НИ НА ЧТО НЕ МЕНЯЙ)."

                        )
                    ),
                    Messages(
                        role=MessagesRole.USER,
                        content=prompt
                    )
                ],
                model=self.model
            )
            logging.debug(f"Отправка запроса: {prompt}")
            response = self.client.chat(chat)
            logging.debug(f"Получен ответ: {response.choices[0].message.content[:100]}...")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Исключение в get_films: {str(e)}")
            return f"Ошибка при запросе к GigaChat: {str(e)}"