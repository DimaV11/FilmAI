from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

class GigaChatAPI:
    def __init__(self, client_secret: str, model: str = "GigaChat"):
        self.client_secret = client_secret
        self.model = model
        self.client = GigaChat(
            credentials=self.client_secret,
            model=self.model,
            verify_ssl_certs=False
        )


    def get_films(self, prompt: str) -> str:
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
        response = self.client.chat(chat)
        return response.choices[0].message.content
