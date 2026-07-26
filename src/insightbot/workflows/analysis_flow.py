"""GroupChat workflow: user -> manager -> planner/coder/executor/reviewer."""
from autogen import ConversableAgent, GroupChat, GroupChatManager

from insightbot.agents.team import build_agents
from insightbot.config.llm_config import llm_config
from insightbot.tools.data_tools import load_csv_summary


def run_analysis(question: str, csv_name: str):
    planner, coder, executor_agent, reviewer = build_agents()

    user_proxy = ConversableAgent(
        "user_proxy",
        llm_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda m: m.get("content")
        and "TERMINATE" in m["content"],
        description="Represents the human user.",
    )

    # group_chat = GroupChat(
    #     agents=[user_proxy, planner, coder, executor_agent, reviewer],
    #     messages=[],
    #     max_round=15,
    #     speaker_selection_method="auto",     # manager's LLM routes (video 11)
    # )
    
# Legal conversation graph: plan -> code -> execute -> review -> (retry or end)
    allowed_transitions = {
        user_proxy:     [planner],
        planner:        [coder],
        coder:          [executor_agent],       # code MUST be executed next
        executor_agent: [reviewer],             # result MUST be reviewed next
        reviewer:       [coder, user_proxy],    # failure -> coder retries; success -> end
    }

    group_chat = GroupChat(
        agents=[user_proxy, planner, coder, executor_agent, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="auto",
        allowed_or_disallowed_speaker_transitions=allowed_transitions,
        speaker_transitions_type="allowed",
    )
    
    # manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        is_termination_msg=lambda m: m.get("content")
        and "TERMINATE" in m["content"],          # <-- manager now stops the chat
    )

    task = (
        f"USER QUESTION: {question}\n\n"
        f"DATA SUMMARY:\n{load_csv_summary(csv_name)}\n\n"
        f"CSV file name: {csv_name}"
    )

    return user_proxy.initiate_chat(
        manager, message=task, summary_method="reflection_with_llm"
    )
