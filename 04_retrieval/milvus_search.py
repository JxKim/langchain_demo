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
        param={"nprobe":10}
    )

    dense_request = AnnSearchRequest(
        data=[query_dense_vector],
        anns_field="vector",
        limit=top_k,
        param={"nprobe":10}
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
        output_fields=["metadata"]
    )

    return res


client = MilvusClient(uri="http://localhost:19530",token="")
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