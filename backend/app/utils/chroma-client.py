import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()

class ChromaClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            persist_dir = os.getenv('CHROMA_PERSIST_DIR', './chroma_db')
            cls._instance.client = chromadb.PersistentClient(
                path=persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
            cls._instance.collection = cls._instance.client.get_or_create_collection(
                name="threat_intelligence",
                metadata={"description": "CVE and threat intelligence data"}
            )
        return cls._instance
    
    def get_collection(self):
        return self.collection
    
    def get_client(self):
        return self.client

# Singleton instance
chroma_client = ChromaClient()