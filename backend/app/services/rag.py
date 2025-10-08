from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.utils.chroma_client import chroma_client
from app.services.embeddings import EmbeddingService
import os

class RAGService:
    def __init__(self):
        self.collection = chroma_client.get_collection()
        self.embedding_service = EmbeddingService()
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
    
    def ingest_cves(self, cves: List[Dict]):
        """Ingest CVEs into ChromaDB"""
        
        if not cves:
            return
        
        documents = []
        metadatas = []
        ids = []
        
        for cve in cves:
            documents.append(cve['content'])
            metadatas.append({
                'cve_id': cve['cve_id'],
                'severity': cve['severity'],
                'cvss_score': str(cve['cvss_score']),
                'published_date': cve['published_date']
            })
            ids.append(cve['cve_id'])
        
        # Generate embeddings
        embeddings = self.embedding_service.create_embeddings(documents)
        
        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Ingested {len(cves)} CVEs into ChromaDB")
    
    def query(self, user_query: str, top_k: int = 5) -> Dict:
        """Query the RAG system"""
        
        # Generate query embedding
        query_embedding = self.embedding_service.create_query_embedding(user_query)
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        if not results['documents'][0]:
            return {
                'answer': "I couldn't find any relevant threat intelligence for your query.",
                'sources': []
            }
        
        # Prepare context
        context_docs = results['documents'][0]
        context_metadata = results['metadatas'][0]
        
        context = "\n\n".join([
            f"CVE ID: {meta['cve_id']}\n"
            f"Severity: {meta['severity']} (CVSS: {meta['cvss_score']})\n"
            f"Description: {doc}"
            for doc, meta in zip(context_docs, context_metadata)
        ])
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a cybersecurity threat intelligence analyst. 
            Based on the provided CVE data, answer the user's question clearly and concisely.
            
            Always include:
            1. A summary of relevant threats
            2. Severity levels
            3. Affected systems (if mentioned)
            4. Recommended actions or mitigations (if applicable)
            5. CVE IDs as citations
            
            Be precise and security-focused."""),
            ("user", """Context from CVE database:
            {context}
            
            Question: {question}
            
            Provide a clear answer with specific CVE citations.""")
        ])
        
        # Generate response
        chain = prompt | self.llm
        response = chain.invoke({
            "context": context,
            "question": user_query
        })
        
        # Format sources
        sources = [
            {
                'cve_id': meta['cve_id'],
                'severity': meta['severity'],
                'cvss_score': meta['cvss_score']
            }
            for meta in context_metadata
        ]
        
        return {
            'answer': response.content,
            'sources': sources
        }