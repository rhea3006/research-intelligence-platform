from api.services.llm_service import llm

response = llm.generate_response(
    "Say hello in exactly one sentence."
)

print(response)