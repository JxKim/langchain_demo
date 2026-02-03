def text_splitter_demo():

    # 1、引入
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # 2、构造实例
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["", "\n","。"],
        chunk_size=500,
        length_function=len,
        chunk_overlap=100
        )
    
    # 3、准备大Document对象
    from langchain_community.document_loaders import UnstructuredWordDocumentLoader
    my_path = r'D:\PycharmProjects\lessons\demo_class\LangChainDemo\04_retrieval\assets\sample.docx'
    loader = UnstructuredWordDocumentLoader(file_path=my_path,mode="single")
    document_list = loader.load()
    document = document_list[0]
     
    # 4、切分Document对象
    chunks_str = text_splitter.split_text(document.page_content)

    for chunk in chunks_str:
        print(chunk)
        print("="*50)

text_splitter_demo()