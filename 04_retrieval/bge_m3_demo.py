from FlagEmbedding import BGEM3FlagModel

# 1、构造一个model

model = BGEM3FlagModel(model_name_or_path="./assets/models/bge-m3")

# 2、准备文本数据
texts =["标量字段通常用来存储一些元数据，并可以在搜索时通过元数据进行过滤"]


# 3、调用model.encode方法
all_embeddings = model.encode(texts,return_dense=True,return_sparse=True)

# 4、稠密向量
dense_vectors = all_embeddings['dense_vecs']
print(dense_vectors[0])

# 5、稀疏向量
sparse_vectors = all_embeddings["lexical_weights"]
print(sparse_vectors[0])
print(model.convert_id_to_token(sparse_vectors[0]))
