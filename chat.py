from getpass import getpass
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import HuggingFaceEmbeddings
import os

#os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
#openAI.api_key = os.getenv("OPENAI_API_KEY").replace("'", "")


# add the path to the CV as a PDF
loader = TextLoader('data.txt')
# Embed the document and store into chroma DB
index = VectorstoreIndexCreator(embedding= HuggingFaceEmbeddings()).from_loaders([loader])


# # specify the path to the .bin downloaded file
# local_path = './models/ggml-gpt4all-j-v1.3-groovy.bin'  # replace with your desired local file path
# # Callbacks support token-wise streaming
# callbacks = [StreamingStdOutCallbackHandler()]
# # Verbose is required to pass to the callback manager
# llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True, backend='gptj')

from pathlib import Path
question = Path('new_query_gas.txt').read_text()
question_1 = str(question)
print(question_1)
#question = str(input("Please enter your question: "))
# perform similarity search and retrieve the context from our documents
results = index.vectorstore.similarity_search(question_1, k=2)
# join all context information (top 4) into one string 
context = "\n".join([document.page_content for document in results])
# print(f"Retrieving information related to your question...")
# print(f"Found this content which is most similar to your question: {context}")

template = """
Please use the following context to answer questions.
Context: {context}
---
Question: {question_1}
Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["context", "question_1"]).partial(context=context)
llm = OpenAI(temperature=0)
llm_chain = LLMChain(prompt=prompt, llm=llm)
# Print the result
print("Processing the information with OpenAI...\n")

# E.g, write a shacl ttl file For the cutting process at CNC cutting machines a defined pressure 
# as well as a given flow rate of gas (or different gases, 
# depending on the process) has to be kept. To ensure that these parameters are met, the gas sampling
# point connected to the CNC cutting system is to be equipped with appropriate sensor technology and 
# the values are to be documented. Requires specific window 10 -12 bar at inlet. Input pressure 
# is measured, output pressure is set and output. use the the given context and namespace to write the shacl file.
print(llm_chain.run(question_1))
