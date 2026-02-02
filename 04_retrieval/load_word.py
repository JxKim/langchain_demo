def word_loader_demo():
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    docs = UnstructuredWordDocumentLoader(
        # 文件路径
        file_path="assets/sample.docx",
        # 加载模式:
        #   single 返回单个Document对象
        #   elements 按标题等元素切分文档
        mode="elements",
    ).load()

    for doc in docs[230:260]: # 从文档中间选取30个文档查看结构
        print(doc.page_content)
        print(doc.metadata,end="\n============\n")

if __name__ == "__main__":
    word_loader_demo()
