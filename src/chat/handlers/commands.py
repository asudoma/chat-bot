from typing import Optional


class CommandManager:
    _commands: dict[str, type["CommandHandlerBase"]] = {}
    _singleton: Optional["CommandManager"] = None

    @classmethod
    def singleton(cls) -> "CommandManager":
        if cls._singleton is None:
            cls._singleton = CommandManager()
            cls._singleton.register("/start", StartCommandHandler)
        return cls._singleton

    @classmethod
    def register(cls, command: str, handler: type["CommandHandlerBase"]) -> None:
        cls._commands[command] = handler

    @classmethod
    def get_handler(cls, command: str, *args, **kwargs) -> "CommandHandlerBase":
        handler_class = cls._commands.get(command, UnknownCommandHandler)
        return handler_class(*args, **kwargs)


class CommandHandlerBase:
    def __init__(self, *args, **kwargs):
        pass

    async def process(self) -> str:
        raise NotImplementedError


class StartCommandHandler(CommandHandlerBase):
    async def process(self) -> str:
        return (
            "Привет! 😃 Я ваш дружелюбный текстовый бот, всегда готов помочь с любыми задачами. "
            "Вопросы, идеи или просто поболтать — я всегда здесь для вас!\n"
            "Пока что могу общаться только текстом, но скоро у меня появится еще больше возможностей, "
            "и тогда наше общение станет еще круче. Если что-то нужно или есть вопросы, не стесняйся, пиши! 😊\n"
            "Кстати, как тебя зовут?"
        )


class UnknownCommandHandler(CommandHandlerBase):
    async def process(self) -> str:
        return "Пока, к сожалению, такой команды не знаю 😊"
