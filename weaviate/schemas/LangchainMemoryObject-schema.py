langchain_memory_object_schema = {
    "class": "LangchainMemoryObject",
    "description": "A flexible schema for storing various types of memory objects related to Langchain activities.",
    "properties": [
        {
            "name": "id",
            "dataType": ["string"],
            "description": "A unique identifier for the memory object."
        },
        {
            "name": "content",
            "dataType": ["blob", "text"],
            "description": "The primary content of the memory object, supporting both binary and text data."
        },
        {
            "name": "timestamp",
            "dataType": ["dateTime"],
            "description": "The creation or last modified timestamp of the memory object."
        },
        {
            "name": "tags",
            "dataType": ["string[]"],
            "description": "A set of tags for categorization and retrieval purposes."
        },
        {
            "name": "metadata",
            "dataType": ["text"],
            "description": "Additional metadata as a JSON string, offering flexibility for various use cases."
        }
    ]
}
