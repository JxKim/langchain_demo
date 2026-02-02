def markdown_loader_demo():

    # 1、引入DocumentLoader
    from langchain_community.document_loaders import UnstructuredMarkdownLoader


    # 2、构造DocumentLoader的实例对象
    file_path = r'D:\PycharmProjects\lessons\demo_class\LangChainDemo\04_retrieval\assets\sample.md'
    loader = UnstructuredMarkdownLoader(file_path=file_path,
                                        mode="elements",
                                        )
    
    document = loader.load()

    for doc in document:
        print('当前的元数据信息为：',doc.metadata)
        print('当前的文档内容为',doc.page_content)
        print("="*50)

    return document


from typing import List
from langchain_core.documents import Document
def enrich_document_info(document_list:List[Document]):

    # 维护一个栈，用来存放历史的标题 [(category_depth,title)]
    stack= []
    category_depth = 0
    enriched_list= [] # 用来存放处理后的文档
    for doc in document_list:

        if doc.metadata['category'] == 'Title':

            category_depth = doc.metadata['category_depth']

            while stack and stack[-1][0] >= category_depth:
                stack.pop()
            
            stack.append((category_depth,doc.page_content))
        
        else:
            title_level_info = " > ".join([title for _,title in stack])
            doc_dict={
                "meta_data":doc.metadata,
                "content":title_level_info + "\n" + doc.page_content
            }
            enriched_list.append(doc_dict)

    return enriched_list







document = markdown_loader_demo()
enriched_doc_list = enrich_document_info(document)
print("处理后的文档信息如下：")
for doc_dict in enriched_doc_list:
    print(doc_dict['content'])
    print("="*50)