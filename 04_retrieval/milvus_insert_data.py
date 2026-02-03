from pymilvus import MilvusClient,DataType
def get_client():
    return MilvusClient(uri="http://localhost:19530",token="")

def insert_data(client:MilvusClient,collection_name:str):
    """
    构建数据，并插入到collection中
    """

    # 1、加载一个文件:此处以assets/sample.docx文件为例
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    doc_list = UnstructuredWordDocumentLoader("assets/sample.docx",mode="single").load()
    # 2、切分文件
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50,separators=["\n\n","\n","。"])
    splitted_doc_list =text_splitter.split_documents(doc_list)
    splitted_doc_list = splitted_doc_list[0:20]

    # 查看当前文本列表当中最大的文本长度
    max_len = max([len(bytes(doc.page_content.encode("utf-8"))) for doc in splitted_doc_list])
    print('当前最大长度是：',max_len)
    # 3、构建向量：稠密向量，稀疏向量

    from FlagEmbedding import BGEM3FlagModel

    model = BGEM3FlagModel("assets/models/bge-m3") # 需要安装 带cuda的torch 

    all_vectors = model.encode([doc.page_content for doc in splitted_doc_list],return_dense=True,return_sparse=True)

    dense_vectors = all_vectors["dense_vecs"]
    sparse_vectors = all_vectors['lexical_weights']

    # 4、准备数据：组装成List[Dict]
    insert_data_list=[]
    for  doc, dense_vector, sparse_vector in zip(splitted_doc_list,dense_vectors,sparse_vectors):
        insert_data_list.append({
            "vector":dense_vector,
            "sparse_vector":sparse_vector,
            "metadata":doc.metadata,
            "text":doc.page_content
        })

    # 5、调用client.insert()方法，插入数据
    res = client.insert(
        collection_name=collection_name,
        data=insert_data_list
    )
    # 有多少条数据插入成功
    print(res)

def delete_data(client:MilvusClient,collection_name:str):
    """
    删除collection中的所有数据
    """
    res = client.delete(
        collection_name=collection_name,
        filter="id in [464019606498975723]"
    )
    print(res)

delete_data(client=get_client(),collection_name="demo_collection")