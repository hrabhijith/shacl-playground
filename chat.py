import os
import time
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.llms import OpenAI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import TextLoader

collection_name="knowledgebase"
persist_directory="./.chroma/index"

os.environ["OPENAI_API_KEY"] = 'your key here'

# urls = [ "https://github.com/IndustryFusion/DigitalTwin/blob/main/semantic-model/shacl2flink/tests/sql-tests/kms-constraints/test1/shacl.ttl",
#         "https://github.com/IndustryFusion/DigitalTwin/blob/main/semantic-model/shacl2flink/tests/sql-tests/kms-constraints/test2/shacl.ttl",
#           "https://github.com/IndustryFusion/DigitalTwin/blob/main/semantic-model/shacl2flink/tests/sql-tests/kms-constraints/test5/shacl.ttl",
#             "https://github.com/IndustryFusion/DigitalTwin/blob/main/semantic-model/kms/shacl.ttl",
#             "https://github.com/hrabhijith/shacl-playground/blob/langchain-test/data.txt"]


loader = TextLoader('./data.txt')

# loader = UnstructuredURLLoader(urls=urls)
kb_data = loader.load()

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
kb_doc = text_splitter.split_documents(kb_data)

embeddings = OpenAIEmbeddings()
kb_db = Chroma.from_documents(kb_doc, embeddings, collection_name=collection_name, persist_directory=persist_directory)
kb_db.persist()


prompt_template = """
Please use the following context to answer questions.
Context: {context}
---
Question: {question}
Answer: Let's think step by step."""

chat_history = []
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')
### With an LLM we have the opportunity to give it an identity before a conversation or to define how the question and answer should look like
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(model_name="gpt-3.5-turbo"),
    memory=memory,
    retriever=kb_db.as_retriever(),
    combine_docs_chain_kwargs={'prompt': PROMPT}
)

def chat(question):
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    return(result["answer"])

if __name__ == "__main__":
    while True:
        time.sleep(1)
        question = str(input("Prompt: "))

        print(chat(question))