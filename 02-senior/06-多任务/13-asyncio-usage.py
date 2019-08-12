import asyncio

@asyncio.coroutine
def hello():
	print('hello world')
	yield from asyncio.sleep(1) # yield from 执行其后异步任务
	print('hello again')

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	tasks = [hello(), hello()]
	loop.run_until_complete(asyncio.wait(tasks))