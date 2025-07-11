from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_aws import ChatBedrockConverse

app = FastAPI()

# CORS (to allow React frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; use specific domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize once
llm = ChatBedrockConverse(
    credentials_profile_name="default",
    model="us.deepseek.r1-v1:0",
    temperature=0.1,
    max_tokens=1000,
)
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=2000)
chain = ConversationChain(llm=llm, memory=memory)

# Pydantic input model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    response = chain.invoke({"input": req.message})
    return {"response": response["response"]}
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}
