from langchain_ollama import OllamaEmbeddings

# 'host.docker.internal' permite que o container Docker alcance o Ollama
OLLAMA_BASE_URL = "http://host.docker.internal:11434"
EMBEDDING_MODEL = "mxbai-embed-large"  # Gera vetores de 1024 dimensões


class EmbeddingService:

    @staticmethod
    async def get_embedding(text: str) -> list[float]:
        """
        Gera um embedding vetorial usando o Ollama local.
        Requer que o modelo 'mxbai-embed-large' esteja baixado:
        $ ollama pull mxbai-embed-large
        """
        embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        return await embeddings.aembed_query(text)
