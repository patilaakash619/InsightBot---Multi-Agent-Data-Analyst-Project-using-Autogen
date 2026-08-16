"""All agents for the analysis team (Planner -> Coder -> Executor -> Reviewer)."""
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

from insightbot.config.llm_config import llm_config
from insightbot.config.settings import DATA_DIR, USE_DOCKER, HITL



def build_agents():
    planner = ConversableAgent(
            "planner",
            system_message=(
                "You are a data-analysis planner.\n"
                "STEP 1: Call the load_csv_summary tool with the CSV file name to "
                "inspect the data (use list_datasets if the file name is unknown).\n"
                "STEP 2: After seeing the summary, produce a SHORT numbered plan "
                "(max 4 steps) for the coder. Do NOT write code yourself."
            ),
            llm_config=llm_config,
            human_input_mode="NEVER",
            description="Inspects the data via tools, then creates the analysis plan. Call FIRST.",
        )

    coder = ConversableAgent(
        "coder",
        system_message=(
            "You are a Python data analyst. Write ONE complete python code block "
            "(```python ... ```) that fully answers the plan.\n"
            "Rules:\n"
            "- The CSV is at 'uploads/<file_name>' relative to the working dir.\n"
            "- Save every chart to 'outputs/<name>.png' (matplotlib, no plt.show()).\n"
            "- Print the key numeric findings.\n"
            "- If execution failed, fix the code and resend the full block."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
        description="Writes python code for the plan, or fixes failed code.",
    )

    # --- executor: switch local <-> docker with one env var (videos 4 & 5) ---
    if USE_DOCKER:
        from autogen.coding import DockerCommandLineCodeExecutor
        executor = DockerCommandLineCodeExecutor(
            image="python:3.12-slim", timeout=120, work_dir=str(DATA_DIR)
        )
    else:
        executor = LocalCommandLineCodeExecutor(timeout=60, work_dir=str(DATA_DIR))

    executor_agent = ConversableAgent(
            "executor_agent",
            llm_config=False,
            code_execution_config={"executor": executor},
            human_input_mode="ALWAYS" if HITL else "NEVER",   # <-- Ch. 3 pattern
            description="Executes the coder's python code and returns the output.",
        )

    # reviewer = ConversableAgent(
    #     "reviewer",
    #     system_message=(
    #         "You are a strict reviewer. You NEVER write code yourself.\n"
    #         "Look at the most recent message from executor_agent:\n"
    #         "- If exitcode is 0 AND the user's question is answered AND charts "
    #         "were saved: write a short summary of the findings (with chart "
    #         "filenames) and end with TERMINATE.\n"
    #         "- If exitcode is non-zero (failed): describe the error cause in "
    #         "2-3 sentences addressed to the coder, and DO NOT say TERMINATE. "
    #         "The coder will send corrected code.\n"
    #         "Rule: you may only say TERMINATE right after a SUCCESSFUL execution."
    #     ),
    #     llm_config=llm_config,
    #     human_input_mode="NEVER",
    #     description="Reviews execution results. Summarizes on success; on failure, explains the error so the coder can fix it.",
    # )


    reviewer = ConversableAgent(
        "reviewer",
        system_message=(
            "You are a strict reviewer. You NEVER write code and you NEVER "
            "say TERMINATE - only the Verifier can end the conversation.\n"
            "- If exitcode is 0 and the question is answered: write a short "
            "summary of the findings (with chart filenames) and hand off.\n"
            "- If exitcode is non-zero: describe the error for the coder to fix."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
        description="Reviews execution results and summarizes findings for the Verifier to check.",
    )
    
    verifier = ConversableAgent(
        "verifier",
        system_message=(
            "You are an independent verifier. NEVER trust the Reviewer's claims "
            "blindly. Call the recompute_aggregates tool to get ground-truth "
            "numbers computed directly from the raw CSV.\n"
            "Compare those numbers to the Reviewer's summary:\n"
            "- If they match (or the question wasn't a groupby-aggregate type, "
            "e.g. a single-column stat): confirm and end with TERMINATE.\n"
            "- If they clearly disagree: explain the discrepancy in 2-3 sentences "
            "to the coder and do NOT say TERMINATE.\n"
            "Rule: only YOU may say TERMINATE."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
        description="Independently re-checks the reviewer's numbers against the raw data before ending.",
    )   

    return planner, coder, executor_agent, reviewer, verifier
