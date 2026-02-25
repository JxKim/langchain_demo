import os
from pathlib import Path
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())



fs_backend = FilesystemBackend(root_dir="05_agents")

llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai"
)


agent = create_deep_agent(
    model=llm,

    backend=fs_backend,

    skills=["skills"],
    checkpointer=MemorySaver(),

    system_prompt=" you are a helpful assistant"
)



def run_demo():

    
    bad_code = """
        def get_user(user_id):
            import sqlite3
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE id = " + user_id
            cursor.execute(sql)
            return cursor.fetchall()
    """
    

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": f"Please help me review the following code using the code-reviewer skill: {bad_code}.If there is any issue, please point it out."}
        ],
    }, config={"configurable": {"thread_id": "skill_demo_v3"}})

    print(result["messages"][-1].content)

if __name__ == "__main__":
    run_demo()
