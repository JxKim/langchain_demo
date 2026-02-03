import asyncio
# 1、定义协程函数一：
async def coroutine_1():

    print("开始执行coroutine_1")

    # await 等待
    await asyncio.sleep(5)

    print("继续执行coroutine_1")

# 2、定义协程函数二：
async def coroutine_2():

    print("开始执行coroutine_2")

    # await 等待
    await asyncio.sleep(7)

    print("继续执行coroutine_2")

# 3、定义协程函数三：
async def coroutine_3():

    print("开始执行coroutine_3")

    # await 等待
    await asyncio.sleep(7)

    print("继续执行coroutine_3")



async def main():

    # # 获取协程：直接调用协程函数
    # coroutine_task = coroutine_1()

    # 以下这种方式，其实还是什么串行执行，只是用await等待了一下
    # coroutine_task1 = await coroutine_1()

    # coroutine_task2 = await coroutine_2()

    # coroutine_task3 = await coroutine_3()

    # 并发执行三个执行：使用asyncio.gather()
    big_coroutine_task = asyncio.gather(
        coroutine_1(),
        coroutine_2(),
        coroutine_3(),
    )

    await big_coroutine_task

if __name__=="__main__":
    import asyncio 
    asyncio.run(main())