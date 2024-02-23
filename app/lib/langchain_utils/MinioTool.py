from langchain.tools import BaseTool
from minio import Minio
from minio.error import S3Error

class MinioTool(BaseTool):
    name = "minio"
    description = "Interact with MinIO object storage."

    def __init__(self, minio_url, access_key, secret_key, secure=False):
        """
        Initialize the MinIO client.
        :param minio_url: URL of the MinIO server.
        :param access_key: Access key for MinIO.
        :param secret_key: Secret key for MinIO.
        :param secure: Use secure connection.
        """
        try:
            self.minio_client = Minio(minio_url, access_key=access_key, secret_key=secret_key, secure=secure)
        except Exception as e:
            raise ValueError(f"Failed to initialize MinioTool: {e}")

    def _run(self, action, bucket_name, object_name, **kwargs):
        """
        Perform the specified action with MinIO. Supports 'upload', 'download', 'list'.
        :param action: The action to perform ('upload', 'download', 'list').
        :param bucket_name: Name of the bucket.
        :param object_name: Name of the object.
        :return: Result of the action.
        """
        try:
            if action == 'upload':
                return self.upload_file(bucket_name, object_name, **kwargs)
            elif action == 'download':
                return self.download_file(bucket_name, object_name, **kwargs)
            elif action == 'list':
                return self.list_objects(bucket_name)
            else:
                return {"error": f"Action '{action}' not supported"}
        except S3Error as e:
            return {"status": "error", "message": str(e)}
            
    def upload_file(self, bucket_name, object_name, file_path):
        try:
            self.minio_client.fput_object(bucket_name, object_name, file_path)
            return {"status": "success", "message": f"File {file_path} uploaded as {object_name} in bucket {bucket_name}"}
        except S3Error as e:
            return {"status": "error", "message": str(e)}

    def download_file(self, bucket_name, object_name, file_path):
        try:
            self.minio_client.fget_object(bucket_name, object_name, file_path)
            return {"status": "success", "message": f"File {object_name} downloaded from bucket {bucket_name} to {file_path}"}
        except S3Error as e:
            return {"status": "error", "message": str(e)}

    def list_objects(self, bucket_name):
        try:
            objects = self.minio_client.list_objects(bucket_name)
            return {"status": "success", "objects": [obj.object_name for obj in objects]}
        except S3Error as e:
            return {"status": "error", "message": str(e)}

# Example usage
#minio_tool = MinioTool(minio_url="minio.example.com", access_key="YOUR_ACCESS_KEY", secret_key="YOUR_SECRET_KEY", secure=False)
# Upload a file
#upload_result = minio_tool.run("upload", "my-bucket", "object-name", file_path="/path/to/file")
# Download a file
#download_result = minio_tool.run("download", "my-bucket", "object-name", file_path="/path/to/download")
# List objects in a bucket
#list_result = minio_tool.run("list", "my-bucket", "object-name")

#In this example:
#- `MinioTool` is derived from `BaseTool`.
#- The `__init__` method initializes the MinIO client with the provided credentials and endpoint.
#- The `run` method acts as a router for different actions (`upload`, `download`, `list`).
#- Separate methods handle each action, like `upload_file`, `download_file`, and `list_objects`.
#- Error handling is implemented using `try-except` blocks around MinIO operations.

#You'll need to install the `minio` Python package (`pip install minio`) and replace the placeholders (`minio.example.com`, `YOUR_ACCESS_KEY`, `YOUR_SECRET_KEY`) with your MinIO instance's details. Also, ensure that the actions and their implementations align with your specific requirements for interacting with MinIO.