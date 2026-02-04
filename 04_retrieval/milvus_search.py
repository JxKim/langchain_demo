from pymilvus import MilvusClient
def dense_vector_search(client:MilvusClient,collection_name:str,query_vector:list,top_k:int=3):
    """
    基于稠密向量进行搜索
    """

    res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        anns_field="vector",
        limit=top_k,
        metric_type="COSINE",
        output_fields=["metadata"]
    )

    if res:
        result = res[0]
        print(result)
        return result
    
def sparse_vector_search(client:MilvusClient,collection_name:str,query_vector:dict,top_k:int=3):
    """
    基于稀疏向量进行搜索
    """

    res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        anns_field="sparse_vector",
        limit=top_k,
        metric_type="IP",
        output_fields=["metadata"]
    )

    if res:
        result = res[0]
        print(result)
        return result
    

def hybrid_search(client:MilvusClient,collection_name:str,query_sparse_vector:dict,query_dense_vector:list,top_k:int=3):
    """
    基于稠密向量和稀疏向量进行混合检索
    """

    # 1、引入Milvus当中的AnnsRequest类
    from pymilvus import AnnSearchRequest


    # 2、构建AnnSearchRequest对象：包含了稠密向量检索和稀疏向量检索
    sparse_request = AnnSearchRequest(
        data=[query_sparse_vector],
        anns_field="sparse_vector",
        limit=top_k,
        param={}
    )

    dense_request = AnnSearchRequest(
        data=[query_dense_vector],
        anns_field="vector",
        limit=top_k,
        param={}
    )

    # 3、构造reranker对象：RRFReranker
    from pymilvus import RRFRanker

    reranker = RRFRanker()

    # 3、通过调用client.hybrid_search()方法，进行混合检索

    res = client.hybrid_search(
        collection_name=collection_name,
        reqs=[sparse_request,dense_request],
        ranker=reranker,
        limit=top_k,
        output_fields=["metadata","text"]
    )

    # 返回的结构[{"entity":{"metadata":"xx","text":"xxx"}},{},{}]
    return res[0]


def scalar_query_examples(client,collection_name:str, like_keyword: str = "大模型"):
    # 对text字段进行检索
    try:
        like_res = client.query(
            collection_name=collection_name,
            filter=f'text like "%{like_keyword}%"',
            output_fields=["id", "text"],
            limit=5,
        )
        print("\n" + "=" * 20)
        print(f'标量检索（query: text like "%{like_keyword}%"）')
        print("=" * 20)
        for row in like_res:
            print({"id": row.get("id"), "text": row.get("text")})
    except Exception as e:
        print("VARCHAR like 过滤失败：", e)

    # 对metadata字段进行检索
    try:
        json_res = client.query(
            collection_name=collection_name,
            filter='metadata["source"] like "%sample%"',
            output_fields=["id", "metadata"],
            limit=5,
        )
        print("\n" + "=" * 20)
        print('标量检索（query: metadata["source"] like "%sample%"）')
        print("=" * 20)
        for row in json_res:
            print({"id": row.get("id"), "metadata": row.get("metadata")})
    except Exception as e:
        print("JSON 过滤失败（metadata 结构不匹配或不支持该表达式）：", e)


client = MilvusClient(uri="http://localhost:19530",token="")
def vector_search_demo():
    query = "国家所有权"
    from FlagEmbedding import BGEM3FlagModel
    model = BGEM3FlagModel("assets/models/bge-m3")
    query_vector = model.encode([query],return_dense=True,return_sparse=True)
    dense_vector = query_vector["dense_vecs"][0].tolist()
    sparse_vector = query_vector["lexical_weights"][0]
    search_res= sparse_vector_search(client,collection_name="demo_collection",query_vector=sparse_vector)
    print(search_res)

    # 混合检索：
    print("开始混合检索")
    hybrid_res = hybrid_search(client,collection_name="demo_collection",query_sparse_vector=sparse_vector,query_dense_vector=dense_vector)
    print(hybrid_res)

def scalar_query_demo():
    res = scalar_query_examples(client,collection_name="demo_collection",like_keyword="国家所有权")
    print(res)

def rag_demo():
    user_query = "什么是langchain"
    from langchain_openai import ChatOpenAI
    from FlagEmbedding import BGEM3FlagModel
    model = BGEM3FlagModel("assets/models/bge-m3")
    query_vector = model.encode([user_query],return_dense=True,return_sparse=True)
    dense_vector = query_vector["dense_vecs"][0].tolist()
    sparse_vector = query_vector["lexical_weights"][0]
    llm = ChatOpenAI(model="gpt-3.5-turbo",)
    hybrid_res = hybrid_search(client,collection_name="demo_collection",query_sparse_vector=sparse_vector,query_dense_vector=dense_vector)
    # 从hybrid_res中提取text字段
    text_list = [item["entity"]["text"] for item in hybrid_res]
    full_text = '\n'.join(text_list) if text_list else None
    message_list = [
        {"role":"system","content":"你是一个专业的法律问答机器人，可以基于相关文本内容进行回答。如果文本当中没有相关内容，不能捏造信息，直接回复不知道"},
        {"role":"system","content":f"以下是从知识库当中检索出来的相关文本：{full_text}" if full_text else "当前知识库当中没有相关文本"},
        {"role":"user","content":user_query}
    ]

    res = llm.invoke(message_list)

    print(res.content)

rag_demo()