from os import getuid
from langgraph.types import Command
from app.workflow.graph import WorkflowGraph
from pathlib import Path

graph = WorkflowGraph().build_graph()
user_idea = input("Enter your idea: ")

thread_id = getuid()
config = {'configurable': {'thread_id': thread_id}}

results = graph.invoke({"user_idea" : user_idea,
                "requirements" : "", "human_response" : "", "current_question" : ""},
                config = config
    )

while "__interrupt__" in results:
    question = results["__interrupt__"][0].value["message"]
    print(f"Missing information: {question}")
    answer = input("Please provide the missing information: ")
    results = graph.invoke(
        Command(resume = answer),
        config = config
    )


print("Final Results:")
print(results)