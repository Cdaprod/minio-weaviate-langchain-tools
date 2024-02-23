# main.py

import sys
import json
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import FastAPI, Request
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

# Assuming LangChain core functionalities are similarly structured
# For runnables, tools, and creating agents, adjust according to the new package structure
from langchain_core.runnables import Runnable


from langchain_core._api import deprecated
from langchain_core.callbacks import BaseCallbackManager
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool

from langchain.agents.agent import Agent, AgentOutputParser
from langchain.agents.agent_types import AgentType
from langchain.agents.conversational.output_parser import ConvoOutputParser
from langchain.agents.conversational.prompt import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain.agents.utils import validate_tools_single_input
from langchain.chains import LLMChain

# Example for creating an OpenAI functions agent, adjust the import based on actual package structure and naming
from langchain.agents.openai_tools.base import create_openai_tools_agent
# Adjust the imports based on your project structure
from lib.config import app_config, langchain_config, llm_config, tool_config
from lib.langchain_utils.MinioTool import MinioTool
from lib.langchain_utils.WeaviateTool import WeaviateTool
from lib.weaviate_operations import WeaviateOperations
from lib.minio_operations import load_documents_from_minio

app = FastAPI(
    title="Cdaprod AI API Gateway",
    version="1.0",
    description="An api server using Langchain's Runnable interfaces",
)

# Weaviate and MinIO connection details, ensure these are correctly configured
WEAVIATE_ENDPOINT = "http://weaviate:8080"
MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = "minio"
MINIO_SECRET_KEY = "minio123"
MINIO_BUCKET = "langchain-bucket"

llama = Ollama(model="llama2")

class MinioEvent(BaseModel):
    eventName: str
    bucket: dict
    object: dict

class MinioBucket(BaseModel):
    name: str
    owner: Optional[str] = None
    creationDate: Optional[str] = None

class MinioObject(BaseModel):
    key: str
    size: int
    contentType: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    bucket: Optional[MinioBucket] = None

class MinioPath(BaseModel):
    path: str
    parentPath: Optional[str] = None
    objects: List[MinioObject] = Field(default_factory=list)

class MinioFile(BaseModel):
    key: str
    size: int
    contentType: Optional[str] = "application/octet-stream"
    metadata: Optional[dict] = Field(default_factory=dict)
    content: Optional[str] = None  # Assuming textual content for simplicity; adjust as needed
    bucket: Optional[MinioBucket] = None

class DocumentProcessingRunnable(Runnable):
    def __init__(self, minio_tool, weaviate_tool):
        self.llm = ChatOpenAI(api_key=llm_config.API_KEY)
        self.weaviate_ops = WeaviateOperations(weaviate_tool.config['url'])
        self.bucket_name = MINIO_BUCKET
        self.minio_ops = lambda: load_documents_from_minio(self.bucket_name, minio_tool.config['endpoint'], minio_tool.config['access_key'], minio_tool.config['secret_key'])

    def run(self, _):
        documents = self.minio_ops()

        for doc in documents:
            processed_doc = self.process_document(doc)
            doc_name = self.extract_document_name(processed_doc)
            self.weaviate_ops.index_document(self.bucket_name, doc_name, processed_doc)

    def process_document(self, document):
        prompt = f"Process this document: {document}"
        response = self.llm.complete(prompt=prompt)
        return response

    def extract_document_name(self, document):
        return "ExtractedDocumentName"

def initialize_tools():
    """
    Initialize and return instances of MinioTool and WeaviateTool.
    """
    minio_tool = MinioTool(minio_url=tool_config.MINIO_ENDPOINT,
                           access_key=tool_config.MINIO_ACCESS_KEY,
                           secret_key=tool_config.MINIO_SECRET_KEY,
                           secure=False)  # Set secure=True if using HTTPS
    weaviate_tool = WeaviateTool(tool_config.WEAVIATE_ENDPOINT, tool_config.WEAVIATE_API_KEY)
    return minio_tool, weaviate_tool

# def setup_document_processing_runnable():
#     """
#     Setup DocumentProcessingRunnable with MinioTool and WeaviateTool.
#     """
#     minio_tool, weaviate_tool = initialize_tools()
#     runnable = DocumentProcessingRunnable(minio_tool, weaviate_tool)
#     return runnable

# runnable = setup_document_processing_runnable()

add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)

add_routes(
    app,
    llama(),
    path="/llama2",
)

model = ChatAnthropic()
prompt = ChatPromptTemplate.from_template("Fetch")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

@app.get("/")
async def root():
    return {"message": "LangChain-Weaviate-MinIO Integration Service"}

@app.post("/index_from_minio")
async def index_from_minio():
    runnable.run(None)
    return {"status": "Indexing complete"}

@app.post("/query")
async def query_weaviate(query: str):
    return runnable.weaviate_ops.query_data(query)

@app.post("/update/{uuid}")
async def update_document(uuid: str, update_properties: dict):
    runnable.weaviate_ops.update_document(uuid, update_properties)
    return {"status": "Document updated"}

@app.delete("/delete/{uuid}")
async def delete_document(uuid: str):
    runnable.weaviate_ops.delete_document(uuid)
    return {"status": "Document deleted"}
    
# Existing setup for LangChain, LangServe, and Weaviate...



@app.post("/minio-event")
async def handle_minio_event(event: MinioEvent):
    # Process the MinIO event and extract relevant data
    bucket_name = event.bucket["name"]
    object_key = event.object["key"]
    object_size = event.object["size"]
    content_type = event.object.get("contentType", "application/octet-stream")
    
    # Here you can add logic to process the event further, for example:
    # - Retrieve the object content from MinIO if necessary
    # - Use LangChain to generate a summary or tags based on the content
    # - Index the object data into Weaviate
    
    return {"message": "Event processed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
