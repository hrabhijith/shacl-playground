from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("API_KEY")

from langchain.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader('./FAQ', glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
docs = loader.load()

#print(docs)
### Texts are not loaded 1:1 into the database, but in pieces, so-called "chunks". 
### We can define the chunk size and the overlap between the chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
)

documents = text_splitter.split_documents(docs)
#print(documents[0])

### Texts are not stored as text in the database, but as a vector representation station. 
### Embeddings are a type of word representation that represent the semantic meaning of words in a vector space.
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)

from langchain.vectorstores.faiss import FAISS
import pickle

vectorstore = FAISS.from_documents(documents, embeddings)

### Loading the database Before using the database, it must of course be reloaded.
with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)

with open("vectorstore.pkl", "rb") as f:
    vectorstore = pickle.load(f)

from langchain.prompts import PromptTemplate

prompt_template = """
Please use the following context to answer questions.
Context: {context}
---
Question: {question}
Answer: Let's think step by step."""

#prompt = PromptTemplate(template=template, input_variables=["context", "question_1"]).partial(context=context)
#llm = OpenAI(temperature=0)
#llm_chain = LLMChain(prompt=prompt, llm=llm)

### With an LLM we have the opportunity to give it an identity before a conversation or to define how the question and answer should look like
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

### With chain classes you can easily influence the behavior of the LLM
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

chain_type_kwargs = {"prompt": PROMPT}

llm = OpenAI(openai_api_key=API_KEY, temperature=0, max_tokens=1000)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever(), chain_type_kwargs=chain_type_kwargs)

#query = "Give me the RDF machine state class and objects for IFF namespace from knowledge turtle file ?"
#print(qa.run(query))
#print("\n")
#print("\n")

from pathlib import Path
#question = Path('new_query_gas.txt').read_text()
question = Path('test_query.txt').read_text()

query = str(question)

### In the example just shown, each request stands on its own. A great strength of an LLM, however, is that it can take the entire chat history 
### into account when responding. For this, however, a chat history must be built up from the different questions and answers. 
### With different memory classes this is very easy in Langchain.
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')

### Use memory in chains The memory class can now easily be used in a chain. This can be recognized, for example, by the fact that when you speak of "it", the bot understands the rabbit in this context.

from langchain.chains import ConversationalRetrievalChain

qa = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(model_name="text-davinci-003", temperature=0.4, openai_api_key=API_KEY, max_tokens=1000),
    memory=memory,
    retriever=vectorstore.as_retriever(),
    combine_docs_chain_kwargs={'prompt': PROMPT}
)

#print(qa.run(query))
response = qa.run(query)
print(response)
