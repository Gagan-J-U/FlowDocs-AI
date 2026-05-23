from app.prompting.strategies.default_strategy import (
    DefaultStrategy
)

from app.prompting.strategies.teaching_strategy import (
    TeachingStrategy
)

from app.prompting.strategies.debate_strategy import (
    DebateStrategy
)


def get_prompt_strategy(
    mode: str = "default"
):

    mode = mode.lower()

    if mode == "teaching":

        return TeachingStrategy()

    if mode == "debate":

        return DebateStrategy()

    return DefaultStrategy()