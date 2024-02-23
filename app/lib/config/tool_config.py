
# Configuration settings for Weaviate
WEAVIATE_ENDPOINT = 'http://weaviate:8080'
WEAVIATE_API_KEY = ''

# Configuration settings for MinIO
MINIO_ENDPOINT = 'minio:9000'
MINIO_ACCESS_KEY = 'minio'
MINIO_SECRET_KEY = 'minio123'
MINIO_BUCKET = 'langchain-bucket'

# Configuration for tools
minio_tool_config = {
    "minio_url": tool_config.MINIO_ENDPOINT,
    "access_key": tool_config.MINIO_ACCESS_KEY,
    "secret_key": tool_config.MINIO_SECRET_KEY,
    "secure": False  # Set secure=True if using HTTPS
}
weaviate_tool_config = {
    "url": tool_config.WEAVIATE_ENDPOINT,
    "api_key": tool_config.WEAVIATE_API_KEY
}