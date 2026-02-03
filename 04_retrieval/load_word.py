def load_word_demo():

    # 1、导入langchain unstructured.io word loader
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    # 2、构造Loader实例

    docx_loader = UnstructuredWordDocumentLoader(
        file_path="./assets/sample.docx",
        mode="elements"
    )

    # 3、调用loader当中的load()方法

    document_list = docx_loader.load()

    for doc in document_list[230:260]:
        print('doc的元数据信息：')
        print(doc.metadata)
        print("doc的文本内容字符串：")
        print(doc.page_content)
        print("="*50)

load_word_demo()