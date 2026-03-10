from langchain_ollama import OllamaEmbeddings

class EmbeddingService:
    @staticmethod
    async def get_embedding(text: str):
        """
        Gera embeddings localmente usando o Ollama.
        
        Configurações:
        - model: mxbai-embed-large (o mesmo usado no vídeo do Tech With Tim)
        - base_url: aponta para o host do Docker para alcançar o Windows
        """
        embeddings = OllamaEmbeddings(
            model="mxbai-embed-large",
            # 'host.docker.internal' é necessário para que o container Docker 
            # fale com o serviço do Ollama rodando no seu Windows.
            base_url="http://host.docker.internal:11434"
        )
        
        # Gera o vetor numérico real em vez de retornar apenas zeros
        return await embeddings.aembed_query(text)