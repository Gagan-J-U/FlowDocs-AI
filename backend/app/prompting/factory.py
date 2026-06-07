from app.prompting.strategies.default_strategy import (
    DefaultStrategy
)

from app.prompting.strategies.teaching_strategy import (
    TeachingStrategy
)

from app.prompting.strategies.debate_strategy import (
    DebateStrategy
)

from app.prompting.strategies.beginner_strategy import (
    BeginnerStrategy
)

from app.prompting.strategies.intermediate_strategy import (
    IntermediateStrategy
)

from app.prompting.strategies.expert_strategy import (
    ExpertStrategy
)

from app.prompting.strategies.researcher_strategy import (
    ResearcherStrategy
)


def get_prompt_strategy(
    mode: str = "default"
):

    mode = mode.lower()

    if mode == "teaching":

        return TeachingStrategy()

    if mode == "debate":

        return DebateStrategy()

    if mode == "beginner":

        return BeginnerStrategy()

    if mode == "intermediate":

        return IntermediateStrategy()

    if mode == "expert":

        return ExpertStrategy()

    if mode == "researcher":

        return ResearcherStrategy()

    return DefaultStrategy()