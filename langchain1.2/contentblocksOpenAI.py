from langchain.messages import AIMessage

message = AIMessage(
    content=[
        {
            "type": "reasoning",
            "id": "rs_abc123",
            "summary": [
                {"type": "summary_text", "text": "summary 1"},
                {"type": "summary_text", "text": "summary 2"},
            ],
        },
        {"type": "text", "text": "...", "id": "msg_abc123"},
    ],
    response_metadata={"model_provider": "openai"}
)
res=message.content_blocks
print(res)
# [{'type': 'reasoning', 'id': 'rs_abc123', 'summary': [{'type': 'summary_text', 'text': 'summary 1'}, {'type': 'summary_text', 'text': 'summary 2'}]}, {'type': 'text', 'text': '...', 'id': 'msg_abc123'}]