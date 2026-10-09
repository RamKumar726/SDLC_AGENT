from concurrent.futures import thread
from typing import Any
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from langgraph.types import Command
from pydantic import BaseModel, Field
from pathlib import Path
from fastapi.responses import FileResponse, StreamingResponse
import json
import logging
from collections.abc import Iterator

from app.workflow.graph import WorkflowGraph

app = FastAPI(title= "SDLC Aget API")
workflow = WorkflowGraph().build_graph()
logger = logging.getLogger(__name__)



class StartWorkflowRequest(BaseModel):
    user_idea : str = Field(min_length=1)
    enable_streaming : bool = True

class ResumeWorkflowRequest(BaseModel):
    answer : str = Field(min_length=1)
    enable_streaming : bool = True


def sse_event(event: str, payload: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(payload, default=str)}\n\n"


def stream_workflow(
    thread_id: str,
    graph_input: Any,
    config: dict[str, Any],
) -> Iterator[str]:
    yield sse_event("started", {"thread_id": thread_id})

    try:
        for update in workflow.stream(
            graph_input,
            config=config,
            stream_mode="updates",
        ):
            for node_name in update:
                yield sse_event(
                    "progress",
                    {
                        "thread_id": thread_id,
                        "step": node_name.replace("_", " ").capitalize(),
                    },
                )

        snapshot = workflow.get_state(config)
        pending_interrupts = [
            interrupt
            for task in snapshot.tasks
            for interrupt in task.interrupts
        ]

        if pending_interrupts:
            value = pending_interrupts[0].value
            question = (
                value["message"]
                if isinstance(value, dict)
                else str(value)
            )
            yield sse_event(
                "question",
                {"thread_id": thread_id, "question": question},
            )
        else:
            yield sse_event(
                "result",
                {
                    "thread_id": thread_id,
                    "result": snapshot.values,
                },
            )

    except Exception:
        logger.exception("Workflow stream failed for thread %s", thread_id)
        yield sse_event(
            "error",
            {
                "thread_id": thread_id,
                "message": "Workflow failed. Check the API server logs.",
            },
        )

def workflow_response(thread_id, result):
    interruptions = result.get("__interrupt__", [])
    if interruptions:
        interrupt_value = interruptions[0].value
        return{
            "thread_id" : thread_id,
            "question" : interrupt_value['message']
        }
    return{
        "thread_id" : thread_id,
        "result" : result
    }

@app.post("/api/workflows")
def start_workflow(request : StartWorkflowRequest):
    thread_id = str(uuid4())
    config = {"configurable" : {"thread_id" : thread_id}}
    graph_input = {
        "user_idea": request.user_idea,
        "requirements": "",
        "human_response": "",
        "current_question": "",
        "human_responses": {},
    }

    if request.enable_streaming:
        return StreamingResponse(
            stream_workflow(thread_id, graph_input, config),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )


    result = workflow.invoke(
        graph_input,
        config =  config,
    )

    return workflow_response(thread_id, result)

@app.post("/api/workflows/{thread_id}/resume")
def resume_workflow(
    thread_id: str,
    request: ResumeWorkflowRequest,
) -> dict[str, Any]:
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = workflow.get_state(config)

    if not snapshot.values:
        raise HTTPException(status_code=404, detail="Workflow thread not found")

    pending_interrupts = [
    interrupt
    for task in snapshot.tasks
    for interrupt in task.interrupts
    ]

    if not pending_interrupts:
        raise HTTPException(
            status_code=409,
            detail="Workflow is not waiting for a clarification",
        )
    graph_input = Command(resume=request.answer)

    if request.enable_streaming:
        return StreamingResponse(
            stream_workflow(thread_id, graph_input, config),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

    result = workflow.invoke(Command(resume=request.answer), config=config)
    return workflow_response(thread_id, result)

@app.get("/health")
def health():
    return {"Message" : "OK"}

@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
    