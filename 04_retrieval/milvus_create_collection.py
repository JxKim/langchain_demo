from pymilvus import MilvusClient,DataType
def get_client():
    

    return MilvusClient(uri="http://localhost:19530",token="")


def build_schema():
    schema = MilvusClient.create_schema(
        auto_id=True
    ).add_field(
        field_name="id",
        datatype=DataType.INT64,
        is_primary=True
    ).add_field(
        field_name="vector",
        datatype=DataType.FLOAT_VECTOR,
        dim=1024
    ).add_field(
        field_name="sparse_vector",
        datatype=DataType.SPARSE_FLOAT_VECTOR,
    ).add_field(
        field_name="metadata",
        datatype=DataType.JSON
    ).add_field(
        field_name="text",
        datatype=DataType.VARCHAR,
        max_length=1500
    )
    return schema

def build_index():
    index_params = MilvusClient.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="HNSW",
        metric_type="COSINE"
    )
    index_params.add_index(
        field_name="sparse_vector",
        index_type="SPARSE_INVERTED_INDEX",
        metric_type="IP"
    )

    return index_params

def create_collection(client:MilvusClient,collection_name:str):
    client.drop_collection(collection_name=collection_name)
    # 构建collection
    client.create_collection(
        collection_name=collection_name,
        schema=build_schema(),
        index_params=build_index(),
    )

client = get_client()

res = client.list_collections()
create_collection(client=client,collection_name="demo_collection")
