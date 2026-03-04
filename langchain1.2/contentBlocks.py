from langchain.messages import AIMessage

message = AIMessage(
    content=[
        {"type": "thinking", "thinking": "...", "signature": "WaUjzkyp..."},
        {"type": "text", "text": "..."},
    ],
    response_metadata={"model_provider": "anthropic"}
)
res=message.content_blocks
print(res) 
#[{'type': 'reasoning', 'reasoning': '...', 'extras': {'signature': 'WaUjzkyp...'}}, {'type': 'text', 'text': '...'}]
