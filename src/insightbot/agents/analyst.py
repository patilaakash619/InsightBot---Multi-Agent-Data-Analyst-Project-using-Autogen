"""The front-facing Analyst agent - hides the whole team via nested chat (Ch. 10)."""
from autogen import ConversableAgent
from insightbot.config.llm_config import llm_config


def forward_task(recipient, messages, sender, config):
    """Pass the user's message into the nested team chat unchanged."""
    return messages[-1]["content"]


def build_analyst(manager, team_agents):
    analyst = ConversableAgent(
        "analyst",
        system_message=(
            "You are InsightBot, a friendly data analyst. You present final "
            "analysis results to the user clearly and concisely."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    analyst.register_nested_chats(
        [
            {
                "recipient": manager,
                "message": forward_task,
                "max_turns": 1,
                "summary_method": "reflection_with_llm",
            }
        ],
        # fire only on messages from OUTSIDE the team (video 10's trick)
        trigger=lambda sender: sender is None
        or (sender is not manager and sender not in team_agents),
    )
    return analyst