# minio-weaviate-langchain

[Repo URL](https://github.com/cdaprod/minio-weaviate-langchain)

[![CI/CD Pipeline for LangChain-Weaviate-MinIO App](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/deploy-with-selfhosted-runner.yml/badge.svg)](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/deploy-with-selfhosted-runner.yml)

[![Docker Compose Test Build](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/docker-compose-test.yml/badge.svg)](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/docker-compose-test.yml)

[![Docker Compose Test Build and Push to DockerHub](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/docker-compose-and-push.yml/badge.svg)](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/docker-compose-and-push.yml)

### Under Development
[![Python App Test Build](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/python-app-test.yml/badge.svg)](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/python-app-test.yml)

[![Update README with Directory Tree](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/update_readme.yml/badge.svg)](https://github.com/Cdaprod/minio-weaviate-langchain/actions/workflows/update_readme.yml)

## Current Directory Tree Structure
The following directory tree is programatically generated to provide an overview of the repos structure (by using `.github/workflows/update_readme.yml` and `.github/scripts/update_readme.py` and is ran on `push` to `main`):

<!-- DIRECTORY_TREE_START -->
```
.
├── DIRECTORY_TREE.txt
├── LICENSE
├── README.md
├── app
│   ├── Dockerfile
│   ├── README.md
│   ├── __init__.py
│   ├── init_weaviate.py
│   ├── lib
│   │   ├── __init__.py
│   │   ├── agents
│   │   │   ├── AGENTS.md
│   │   │   ├── __init__.py
│   │   │   ├── agents.py
│   │   │   ├── create_agent.py
│   │   │   └── data_agent.py
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   ├── app_config.py
│   │   │   ├── langchain_config.py
│   │   │   ├── llm_config.py
│   │   │   └── tool_config.py
│   │   ├── langchain_utils
│   │   │   ├── Implement-Prompting.md
│   │   │   ├── MinioTool.py
│   │   │   ├── WeaviateTool.py
│   │   │   └── __init__.py
│   │   ├── minio_operations.py
│   │   ├── tools
│   │   │   ├── ResearchTool.py
│   │   │   ├── WritingTool.py
│   │   │   ├── __init__.py
│   │   │   ├── tagging
│   │   │   │   ├── __init__.py
│   │   │   │   └── tagging_with_llm.md
│   │   │   └── weaviate_operations.py
│   │   └── weaviate_operations.py
│   ├── main.py
│   ├── requirements.txt
│   └── setup.py
├── artifact-docker-compose.yaml
├── docker-compose.yaml
├── library
│   ├── chat_agent_executor_with_function_tools.ipynb
│   ├── custom_agent_with_plugin_retrieval.ipynb
│   ├── force-calling-a-tool-first.ipynb
│   ├── hierarchical_agent_teams.ipynb
│   ├── langchain-agents-multiple-tool-chains-together.ipynb
│   ├── langchain-v0-1-0-quickstart-tutorial.ipynb
│   ├── langgraph_crag.ipynb
│   ├── multi-agent-collaboration.ipynb
│   ├── openai_functions_retrieval_qa.ipynb
│   ├── plan-and-execute.ipynb
│   ├── reflection.ipynb
│   ├── sharedmemory_for_tools.ipynb
│   └── web_voyager.ipynb
├── minio
│   ├── Dockerfile
│   ├── data
│   │   └── is_empty
│   └── entrypoint.sh
└── weaviate
    ├── data.json
    ├── dockerfile
    ├── library
    │   └── Getting_Started_With_Weaviate_Python_Client.ipynb
    └── schemas
        ├── Article-Author-schema.json
        └── LangchainMemoryObject-schema.py

13 directories, 56 files

```
<!-- DIRECTORY_TREE_END -->


Creating an "s3-engine" with Weaviate and LangChain's S3 directory loader using LangChain Expression Language (LCEL) and variables instead of functions and classes involves setting up a series of operations as standalone variables or inline expressions. Here's how you can structure it:

To parse and index MarkdownDocument objects into Weaviate using data retrieved from an S3 loader, and processed through an LLM using LangChain Expression Language (LCEL) functionally, we can set up a series of operations as standalone variables or inline lambda functions. Here's a structured approach:

REQUIRED WORKFLOW SECRETS:
- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN
- PYPI_API_TOKEN
- GH_TOKEN

### Step 1: Import Required Modules

```python
from langchain.llms import ChatOpenAI
from langchain_community.document_loaders.s3_directory import S3DirectoryLoader
from weaviate.client import Client
```

### Step 2: Initialize Clients

```python
# Initialize ChatOpenAI LLM
llm = ChatOpenAI(api_key="YOUR_OPENAI_API_KEY")

# Initialize Weaviate Client
weaviate_client = Client("WEAVIATE_ENDPOINT")

# Initialize S3 Directory Loader
s3_loader = S3DirectoryLoader(
    bucket='your-bucket',
    prefix='',
    endpoint_url='your-minio-endpoint',
    aws_access_key_id='your-access-key',
    aws_secret_access_key='your-secret-key',
    use_ssl=False  # or True
)
```

### Step 3: Define Operations as Variables

```python
# Define a function to process documents through the LLM
process_document = lambda doc: llm.invoke({"document": doc})

# Define a function to index documents into Weaviate
index_document = lambda doc: weaviate_client.data_object.create(
    data_object=doc,
    class_name="MarkdownDocument"
)
```

### Step 4: Retrieve, Process, and Index Documents

```python
# Retrieve documents from S3
documents = s3_loader.load()

# Process and index each document
for doc in documents:
    processed_doc = process_document(doc)
    index_document(processed_doc)
```

This setup defines each step in the data processing pipeline as a variable holding a lambda function or a direct function call. This modular approach allows each step (data retrieval, processing, and indexing) to be easily managed and adjusted. Make sure to replace placeholders like `"YOUR_OPENAI_API_KEY"`, `"WEAVIATE_ENDPOINT"`, and S3 loader configurations with your actual details. 

The `process_document` function is a simplification and assumes the LLM can process the document as needed for Weaviate indexing. Depending on your exact requirements, you may need to adjust how the document is processed or how the LLM is invoked.

---
---

To create a functional pipeline using LangChain v0.1.0's LCEL (LangChain Expression Language), where an LLM parses MarkdownDocument objects and indexes them into Weaviate, you can use a combination of PromptTemplates and OutputParsers. The process can be structured as follows:

1. **Initialize the LLM and Output Parsers**: 
   Use LangChain's built-in models and parsers to handle the interaction with the LLM and the parsing of its output. For instance, `OpenAI` or `ChatOpenAI` can be used as the model, and parsers like `JSONOutputParser` or `PydanticOutputParser` can be utilized for parsing the LLM output into structured data.

2. **Define Prompt Template**: 
   Create a PromptTemplate that instructs the LLM to parse the MarkdownDocument. The template should contain the structure of a MarkdownDocument and ask the LLM to return the parsed data in a specified format. The format instructions from the output parser can be included in the template to guide the LLM.

3. **Invoke LLM with the Prompt**: 
   Generate a prompt using the template and invoke the LLM with this prompt. The LLM will return a response based on the template instructions.

4. **Parse the LLM Output**: 
   Use the chosen output parser to parse the LLM's output into a structured format, such as JSON or a Pydantic model.

Here's an example of how this could be implemented functionally:

```python
from langchain.llms import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import JSONOutputParser

# Initialize the LLM
llm = ChatOpenAI(api_key="YOUR_API_KEY")

# Define the Prompt Template
prompt_template = PromptTemplate(
    template="Parse the following MarkdownDocument and return it as structured data:\n\n{markdown_content}\n\nFormat: {format_instructions}",
    input_variables=["markdown_content"],
    partial_variables={"format_instructions": JSONOutputParser().get_format_instructions()}
)

# Example Markdown content
markdown_content = "Your MarkdownDocument content here"

# Generate the prompt
prompt = prompt_template.format(markdown_content=markdown_content)

# Invoke the LLM and get the output
output = llm(prompt)

# Parse the output
parsed_output = JSONOutputParser().parse(output)
```

In this example, `ChatOpenAI` is used as the model, and `JSONOutputParser

In this example, `ChatOpenAI` is used as the model, and `JSONOutputParser` is utilized to parse the LLM's output. The `PromptTemplate` is structured to instruct the LLM to parse the MarkdownDocument content and return it in a structured format. The `JSONOutputParser().get_format_instructions()` method is used to generate format instructions for the LLM, guiding it to produce the output in a structured JSON format.

This approach creates a functional pipeline where the steps of prompting the LLM and parsing its output are encapsulated in variables and lambda functions, aligning with the LangChain's modular and compositional philosophy.

Remember to replace `"YOUR_API_KEY"` with your actual OpenAI API key and `"Your MarkdownDocument content here"` with the actual Markdown content you want to parse. This setup provides a blueprint for creating a pipeline that uses an LLM to parse documents into a structured format suitable for indexing in databases like Weaviate.

---
---

Creating a functional pipeline using LangChain Expression Language (LCEL) and prompt templates to retrieve `MarkdownDocument` content from an S3 directory loader and parse it into a Weaviate schema involves several steps. Let's break down the process:

### Step 1: Setup and Configuration

First, you need to set up the necessary components: the S3 directory loader, the ChatOpenAI LLM, and the Weaviate client.

```python
from langchain.llms import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders.s3_directory import S3DirectoryLoader
from weaviate.client import Client
from minio import Minio

# Initialize MinIO Client for S3 Directory Loader
minio_client = Minio('MINIO_ENDPOINT', access_key='ACCESS_KEY', secret_key='SECRET_KEY', secure=False)

# S3 Directory Loader Setup
s3_directory_loader = S3DirectoryLoader(
    bucket='YOUR_BUCKET_NAME',
    prefix='',
    endpoint_url='MINIO_ENDPOINT',
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY',
    use_ssl=False
)

# Initialize ChatOpenAI LLM
llm = ChatOpenAI(api_key="YOUR_OPENAI_API_KEY")

# Weaviate Client Setup
weaviate_client = Client("WEAVIATE_ENDPOINT")
```

### Step 2: Define Prompt Template

Define a prompt template for processing the Markdown documents:

```python
# Define the prompt template for processing Markdown documents
process_markdown_prompt = PromptTemplate(
    template_string="Parse the following markdown document into a structured format: \n\n{markdown_content}"
)
```

### Step 3: Retrieve and Process Documents

Retrieve documents from the S3 directory loader, process them with the LLM, and parse them into the Weaviate schema.

```python
# Lambda function to load documents
load_documents = lambda: s3_directory_loader.load()

# Lambda function to process documents with LLM
process_document_with_llm = lambda doc: llm.invoke(process_markdown_prompt.format(markdown_content=doc))

# Lambda function to parse the LLM response into Weaviate schema
parse_into_weaviate_schema = lambda llm_response: {
    "metadata": llm_response.get('metadata', {}),
    "tables": llm_response.get('tables', []),
    "code_blocks": llm_response.get('code_blocks', []),
    "content": llm_response.get('content', ''),
    "blob_data": llm_response.get('blob_data', [])
}

# Lambda function to add document to Weaviate
add_to_weaviate = lambda parsed_doc: weaviate_client.data_object.create(
    data_object=parsed_doc, 
    class_name="MarkdownDocument"
)
```

### Step 4: Execute the Pipeline

Finally, execute the pipeline to load, process, and index the documents:

```python
# Loading documents from S3
documents = load_documents()

# Processing each document
for doc in documents:
    llm_response = process_document_with_llm(doc)
    parsed_doc = parse_into_weaviate_schema(llm_response)
    add

to_weaviate(parsed_doc)
```

In this pipeline:

1. Documents are loaded from the S3 directory using the MinIO client.
2. Each document is processed through the LLM using a prompt template to extract structured data.
3. The response from the LLM is parsed into a format suitable for the Weaviate schema.
4. The parsed documents are added to Weaviate.

Note:
- Ensure the prompt template is well-designed to extract the relevant parts of the markdown document, such as metadata, tables, code blocks, and content.
- Adjust the lambda functions and the parsing logic as needed based on the specific structure of your markdown documents and the required Weaviate schema.
- Replace placeholders like `'MINIO_ENDPOINT'`, `'ACCESS_KEY'`, `'SECRET_KEY'`, `'YOUR_BUCKET_NAME'`, `'YOUR_OPENAI_API_KEY'`, and `'WEAVIATE_ENDPOINT'` with your actual configuration details.

This functional approach using LCEL provides a flexible and modular pipeline for processing markdown documents and indexing them into Weaviate, leveraging the capabilities of LangChain and OpenAI's LLM.

---
---

To create Weaviate schemas reflecting the provided classes `SourceCode`, `Table`, and `MarkdownDocument`, you'll need to define them in a format that Weaviate can understand. Weaviate uses a GraphQL-inspired schema definition, so you'll need to translate these Python classes into a suitable schema definition.

Here's how you can define these classes for Weaviate:

### Define the Weaviate Schema

```python
source_code_schema = {
    "class": "SourceCode",
    "properties": [
        {"name": "id", "dataType": ["string"], "description": "Unique identifier for the source code object."},
        {"name": "imports", "dataType": ["string[]"], "description": "List of extracted required packages."},
        {"name": "classes", "dataType": ["string[]"], "description": "List of extracted classes from the code."},
        {"name": "code", "dataType": ["text"], "description": "Source code snippets."},
        {"name": "syntax", "dataType": ["string"], "description": "The programming language syntax/extension."},
        {"name": "context", "dataType": ["text"], "description": "Any extracted text, markdown, comments, or docstrings."},
        {"name": "metadata", "dataType": ["string"], "description": "Metadata tags for code object management."},  # Note: Adjust data type if needed
    ]
}

table_schema = {
    "class": "Table",
    "properties": [
        {"name": "headers", "dataType": ["string[]"], "description": "Headers of the table"},
        {"name": "rows", "dataType": ["string[]"], "description": "Rows of the table, each row being a dictionary"}  # Note: Adjust data type if needed
    ]
}

markdown_document_schema = {
    "class": "MarkdownDocument",
    "properties": [
        {"name": "metadata", "dataType": ["string"], "description": "Metadata of the document"},  # Note: Adjust data type if needed
        {"name": "tables", "dataType": ["Table[]"], "description": "List of tables in the document"},
        {"name": "code_blocks", "dataType": ["SourceCode[]"], "description": "List of code blocks in the document"},
        {"name": "content", "dataType": ["text"], "description": "The textual content of the document"},
        {"name": "blob_data", "dataType": ["blob[]"], "description": "The image or video content of the document"},  # Note: Adjust data type if needed
    ]
}
```

### Add the Schema to Weaviate

Assuming you have a Weaviate client instance (`weaviate_client`), you can add these schemas to Weaviate like this:

```python
weaviate_client.schema.create_class(source_code_schema)
weaviate_client.schema.create_class(table_schema)
weaviate_client.schema.create_class(markdowm_document)
```

---
---

To represent the given Weaviate schemas using Pydantic, you can define Python classes with Pydantic models. These classes will reflect the structure of your Weaviate schemas for `SourceCode`, `Table`, and `MarkdownDocument`. Here's how you can define them:

### Pydantic Models for Weaviate Schemas

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SourceCode(BaseModel):
    id: str = Field(description="Unique identifier for the source code object.")
    imports: List[str] = Field(description="List of extracted required packages.")
    classes: List[str] = Field(description="List of extracted classes from the code.")
    code: str = Field(description="Source code snippets.")
    syntax: str = Field(description="The programming language syntax/extension.")
    context: str = Field(description="Any extracted text, markdown, comments, or docstrings.")
    metadata: Dict[str, Any] = Field(description="Metadata tags for code object management.")

class Table(BaseModel):
    headers: List[str] = Field(description="Headers of the table")
    rows: List[Dict[str, Any]] = Field(description="Rows of the table, each row being a dictionary")

class MarkdownDocument(BaseModel):
    metadata: Dict[str, Any] = Field(description="Metadata of the document")
    tables: List[Table] = Field(description="List of tables in the document")
    code_blocks: List[SourceCode] = Field(description="List of code blocks in the document")
    content: str = Field(description="The textual content of the document")
    blob_data: List[bytes] = Field(description="The image or video content of the document")  # Assuming binary data for blobs
```

In these Pydantic models:

- Each class corresponds to a schema in your Weaviate database.
- The properties of the classes are defined with types and descriptions, mirroring the structure and data types of your Weaviate schemas.
- `List[str]` and `List[Dict[str, Any]]` are used to represent string arrays and dictionaries, respectively.
- For `blob_data` in `MarkdownDocument`, I've used `List[bytes]` assuming binary data for images or videos. Adjust this based on your actual data format.

These Pydantic models can now be used to validate and structure data according to your Weaviate schemas in Python, before indexing them into Weaviate.

---
---

To create a LangChain Runnable that retrieves `MarkdownDocument` content from an S3 directory loader and then parses it using a Pydantic output parser, you can follow these steps:

### Step 1: Define the MarkdownDocument Model with Pydantic

First, define the `MarkdownDocument` class using Pydantic to model the structure of your documents.

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SourceCode(BaseModel):
    # ... definition as provided

class Table(BaseModel):
    # ... definition as provided

class MarkdownDocument(BaseModel):
    # ... definition as provided
```

### Step 2: Set Up the S3 Directory Loader

Initialize the S3 directory loader to retrieve documents from your MinIO (S3 compatible) bucket.

```python
from langchain_community.document_loaders.s3_directory import S3DirectoryLoader

s3_directory_loader = S3DirectoryLoader(
    bucket='your-bucket-name',
    prefix='',
    endpoint_url='your-minio-endpoint',
    aws_access_key_id='your-access-key',
    aws_secret_access_key='your-secret-key',
    use_ssl=False
)
```

### Step 3: Retrieve Documents and Parse with Pydantic

Use the S3 directory loader to retrieve documents. Then, parse each document using the `MarkdownDocument` Pydantic model.

```python
# Function to retrieve and parse documents
retrieve_and_parse_documents = lambda: [
    MarkdownDocument.parse_obj(doc)
    for doc in s3_directory_loader.load()
]

# Example usage
parsed_documents = retrieve_and_parse_documents()
```

### Step 4: Define a LangChain Runnable using LCEL

Create a LangChain Runnable using the LangChain Expression Language to encapsulate the process.

```python
from langchain.runnables import Runnable

# Define a Runnable for processing documents
class ProcessMarkdownDocumentsRunnable(Runnable):
    def invoke(self, _):
        return retrieve_and_parse_documents()

# Initialize the Runnable
process_documents_runnable = ProcessMarkdownDocumentsRunnable()
```

### Step 5: Use the Runnable in Your Workflow

Finally, use the Runnable in your LangChain workflow to process and parse the Markdown documents.

```python
# Process and parse Markdown documents
documents = process_documents_runnable.invoke(None)
```

This setup retrieves Markdown documents from an S3 compatible bucket (MinIO), parses them into a structured format using Pydantic models, and encapsulates the process in a LangChain Runnable. The usage of LCEL and Pydantic models ensures that the data is structured and parsed correctly according to the defined schema.
