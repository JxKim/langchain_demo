def embedding_with_huggingface_demo():

    from langchain_huggingface import HuggingFaceEmbeddings

    # 1、构造一个embed model
    # 使用什么模型，基于多个方面去考虑：1、是否需要多语言支持，2、向量库的负载，能支持多大维度的embedding model
    # 3、需要去做embedding的文本的长度大小
    embed_model = HuggingFaceEmbeddings(model = "./assets/models/bge-base-zh-v1.5")

    # 2、调用embed方法
    res = embed_model.embed_documents(['今天天气很好'])

    print(type(res[0]))
    print(len(res[0]))

def embedding_with_openai_demo():

    from langchain_openai import OpenAIEmbeddings

    # 1、构造一个embed model
    
    embed_model = OpenAIEmbeddings(model = "text-embedding-3-small")

    # 2、调用embed方法
    res = embed_model.embed_documents(['今天天气很好'])

    print(type(res[0]))
    print(len(res[0]))

embedding_with_openai_demo()