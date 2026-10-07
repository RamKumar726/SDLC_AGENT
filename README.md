# SDLC Agent

## Run the API

Start the FastAPI development server from the repository root:

```bash
uv run uvicorn app.api:app --app-dir src --reload
```

The interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Workflow endpoints

- `POST /api/workflows` starts the requirements-to-implementation-plan workflow.
  Send `{"user_idea": "..."}`. The response either contains a `thread_id` and
  a clarification `question`, or a completed `result`.
- `POST /api/workflows/{thread_id}/resume` submits an answer to the outstanding
  clarification. Send `{"answer": "..."}`. If another clarification is needed,
  the response includes the next question; otherwise, it includes the result.

The workflow uses an in-memory LangGraph checkpointer, so clarification sessions
are available only while this server process remains running. Run a single
server worker when using this in-memory configuration.