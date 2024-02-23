from minio import Minio
from typing import List

class MinioOperations:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool = False):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def list_objects_in_bucket(self, bucket_name: str) -> List[str]:
        """
        List all object names in a specified bucket.
        """
        objects = self.client.list_objects(bucket_name)
        return [obj.object_name for obj in objects]

    def get_object_content(self, bucket_name: str, object_name: str) -> str:
        """
        Retrieve the content of a specified object.
        """
        response = self.client.get_object(bucket_name, object_name)
        return response.data.decode('utf-8')

def load_documents_from_minio(bucket: str, endpoint: str, access_key: str, secret_key: str, secure: bool = False) -> List[str]:
    """
    Load documents from a specified MinIO bucket.
    """
    minio_ops = MinioOperations(endpoint, access_key, secret_key, secure)
    object_names = minio_ops.list_objects_in_bucket(bucket)

    documents = []
    for object_name in object_names:
        content = minio_ops.get_object_content(bucket, object_name)
        documents.append(content)

    return documents