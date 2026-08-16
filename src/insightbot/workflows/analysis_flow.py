"""Nested-chat workflow: user -> Analyst -> (hidden) group-chat team."""
from autogen import ConversableAgent, GroupChat, GroupChatManager, register_function

from insightbot.agents.team import build_agents
from insightbot.agents.analyst import build_analyst
from insightbot.config.llm_config import llm_config
from insightbot.tools.data_tools import load_csv_summary, list_datasets, recompute_aggregates


def build_team():
    planner, coder, executor_agent, reviewer, verifier = build_agents()

    user_proxy = ConversableAgent(
        "user_proxy", llm_config=False, human_input_mode="NEVER",
        description="Executes tool calls suggested by the planner and verifier.",
    )

    register_function(load_csv_summary, caller=planner, executor=user_proxy,
                      name="load_csv_summary", description="Get schema, sample rows and stats of a CSV")
    register_function(list_datasets, caller=planner, executor=user_proxy,
                      name="list_datasets", description="List all CSV files available")
    register_function(recompute_aggregates, caller=verifier, executor=user_proxy,
                      name="recompute_aggregates",
                      description="Independently recompute groupby aggregates from the raw CSV")

    team_agents = [user_proxy, planner, coder, executor_agent, reviewer, verifier]

    allowed_transitions = {
        user_proxy:     [planner, verifier],
        planner:        [user_proxy, coder],
        coder:          [executor_agent],
        executor_agent: [reviewer],
        reviewer:       [verifier],
        verifier:       [user_proxy, coder],   # tool call, or retry on mismatch
    }

    group_chat = GroupChat(
        agents=team_agents, messages=[], max_round=18,
        speaker_selection_method="auto",
        allowed_or_disallowed_speaker_transitions=allowed_transitions,
        speaker_transitions_type="allowed",
    )
    manager = GroupChatManager(
        groupchat=group_chat, llm_config=llm_config,
        is_termination_msg=lambda m: m.get("content") and "TERMINATE" in m["content"],
    )
    return manager, team_agents


def run_analysis(question: str, csv_name: str) -> str:
    manager, team_agents = build_team()
    analyst = build_analyst(manager, team_agents)

    task = (
        f"USER QUESTION: {question}\n"
        f"CSV file name: {csv_name}\n"
        f"Planner: start by inspecting the data with your tools."
    )
    reply = analyst.generate_reply(
        messages=[{"role": "user", "content": task}]
    )
    return reply