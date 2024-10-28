import ChromaDbRepository 
import KnowledgeBaseService 
import OpenaiService 
import os
import re
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
caminhoKnowledgeBase = "./knowledge/novoTestamento102PagIZI.pdf"

ChromaDbRepository.InitChroma()
ChromaDbRepository.CreateCollection("collection_bible")


text_complete = KnowledgeBaseService.ler_pdf(caminhoKnowledgeBase)
biblia_dict = KnowledgeBaseService.separar_livro_capitulo_versiculo(text_complete)

# for livroTexto, LivroArray in biblia_dict.items():
#     for capituloNumero, capituloArray in LivroArray.items():
#         for versiculosNumero, versiculosArray in capituloArray.items():
#             #embeddings = OpenaiService.get_embedding(versiculosArray[0])  # Função fictícia para gerar embedding
#             versiculo_id = f"{livroTexto}-{capituloNumero}:{versiculosNumero}"
#             ChromaDbRepository.AddColections(
#                 documents=[versiculosArray[0]],
#                 ids=[versiculo_id],
#                 metadatas=[{"livro": livroTexto, "capitulo": capituloNumero,"versiculo": versiculosNumero}],
#               # embedding=[embeddings]
#             )

print('Para uma melhor acertividade, digite o versículo entre aspas. Exemplo: "Deus é amor"')
pergunta = input('Digite a sua pergunta: ')


embeddingsQuery = OpenaiService.get_embedding(pergunta)  # Função fictícia para gerar embedding

# Se não houver aspas, adicionar a string inteira

#consulta antiga
resultsText = ChromaDbRepository.GetCollectionByQueryText(
    query_texts=pergunta, # Chroma will embed this for you
    n_results=5
    )

#consulta nova teste
resultsEmbedding = ChromaDbRepository.GetCollectionByQueryEmbeddings(
    query_embedding=embeddingsQuery, # Chroma will embed this for you
    n_results=5
    )

system_promptText = """
Você é um ótimo assistente. Você responde perguntas da bíblia e ajuda as pessoas a encontrar versículos completos e capítulos da bíblia de acordo com uma frase e fornece uma explicação sobre aquele versículo

Mas você só pode responder com base no conhecimento que estou lhe fornecendo. Você não usa seu conhecimento interno e não pode inventar coisas.

Se você não sabe a resposta, apenas diga: Eu não consegui encontrar essa informação.
--------------------
The data:
"""+str(resultsText['documents'])+"""
"""+str(resultsText['metadatas'])+"""
"""

system_promptEmbedding = """
Você é um ótimo assistente. Você responde perguntas da bíblia e ajuda as pessoas a encontrar versículos completos e capítulos da bíblia de acordo com uma frase e fornece uma explicação sobre aquele versículo

Mas você só pode responder com base no conhecimento que estou lhe fornecendo. Você não usa seu conhecimento interno e não pode inventar coisas.

Se você não sabe a resposta, apenas diga: Eu não consegui encontrar essa informação.
--------------------
The data:
"""+str(resultsEmbedding['documents'])+"""
"""+str(resultsEmbedding['metadatas'])+"""
"""

responseText = OpenaiService.openai_CHATGPT(system_prompt=system_promptText, user_query=pergunta)

responseEmbedding = OpenaiService.openai_CHATGPT(system_prompt=system_promptEmbedding, user_query=pergunta)


print("\n\n---------------------")
print("Response query by text\n\n")

print(responseText)

print("\n\n---------------------\n\n")

print("\n\n---------------------")
print("Response query by Embedding\n\n")

print(responseEmbedding)

print("\n\n---------------------\n\n")
