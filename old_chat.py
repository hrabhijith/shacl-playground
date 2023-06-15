import os

import weaviate
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Weaviate

# Note. alternatively you can set a temporary env variable like this:
# os.environ["OPENAI_API_KEY"] = 'your-key-goes-here'

if os.getenv("OPENAI_API_KEY") is not None:
    print ("OPENAI_API_KEY is ready")
else:
    print ("OPENAI_API_KEY environment variable not found")

loader = TextLoader("./input.txt")
documents = loader.load()


text_splitter = CharacterTextSplitter(
    chunk_size=500, chunk_overlap=0, length_function=len
)
docs = text_splitter.split_documents(documents)

# Connect to your Weaviate instance
client = weaviate.Client(
    # url="https://your-wcs-instance-name.weaviate.network/",
    url="http://172.22.42.95:8080/",
    # auth_client_secret=weaviate.auth.AuthApiKey(api_key="<YOUR-WEAVIATE-API-KEY>"), # comment out this line if you are not using authentication for your Weaviate instance (i.e. for locally deployed instances)
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    }
)

# Check if your instance is live and ready
# This should return `True`
client.is_ready()


client.schema.delete_all()
client.schema.get()

# Define the Schema object to use `text-embedding-ada-002` on `title` and `content`, but skip it for `url`
article_schema = {
    "classes": [
        {
            "class": "Usecases",
            "description": "A written paragraph",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {"text2vec-openai": {"model": "ada", "type": "text"}},
            "properties": [
                {
                    "dataType": ["text"],
                    "description": "The content of the paragraph",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False,
                        }
                    },
                    "name": "content",
                },
            ],
        },
    ]
}

# add the Article schema
client.schema.create(article_schema)

vectorstore = Weaviate(client, "Usecases", "content")


text_meta_pair = [(doc.page_content, doc.metadata) for doc in docs]

texts, meta = list(zip(*text_meta_pair))

vectorstore.add_texts(texts, meta)

query = "pressure window"
docs = vectorstore.similarity_search(query)


for doc in docs:
    print(doc.page_content)