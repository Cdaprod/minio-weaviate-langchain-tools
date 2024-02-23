from weaviate.client import Client
from .minio_operations import load_documents_from_minio

class WeaviateOperations:
    def __init__(self, weaviate_endpoint: str):
        self.client = Client(weaviate_endpoint)

    def index_document(self, bucket_name: str, document_name: str, document_content: str):
        """
        Indexes a document into Weaviate.
        """
        data_object = {
            "name": document_name,
            "content": document_content
        }
        self.client.data_object.create(data_object=data_object, class_name="MarkdownDocument")

    def index_documents_from_minio(self, bucket: str, minio_endpoint: str, access_key: str, secret_key: str, secure: bool = False):
        """
        Retrieve documents from MinIO and index them into Weaviate.
        """
        documents = load_documents_from_minio(bucket, minio_endpoint, access_key, secret_key, secure)
        for doc_content in documents:
            # Assuming doc_content contains necessary identifiers or names
            doc_name = self.extract_name_from_content(doc_content)
            self.index_document(bucket, doc_name, doc_content)

    @staticmethod
    def extract_name_from_content(content: str) -> str:
        """
        Extracts or assigns a name to a document based on its content.
        """
        # Implement logic to extract a name or identifier from the document content
        # For example, you might extract the first line as a name, or use a UUID
        return "ExtractedNameOrIdentifier"
        
    def query_data(self, query):
        """
        Query data from Weaviate.
        """
        return self.client.query.get(query)

    def update_document(self, uuid, update_properties):
        """
        Update a document in Weaviate.
        """
        self.client.data_object.update(
            uuid=uuid,
            data_object=update_properties,
            class_name="MarkdownDocument"
        )

    def delete_document(self, uuid):
        """
        Delete a document from Weaviate.
        """
        self.client.data_object.delete(uuid, class_name="MarkdownDocument")