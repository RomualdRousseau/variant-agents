import vertexai

client = vertexai.Client()
#  project="PROJECT_ID",
#  location="LOCATION"
# )

# If you don't have an Agent Engine instance already, create an instance.
agent_engine = client.agent_engines.create()

# Print the agent engine ID, you will need it in the later steps to initialize
# the ADK `VertexAiSessionService`.
print(agent_engine.api_resource.name.split("/")[-1])
