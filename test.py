import asyncio

import libs.User as User


async def main():
    # Your asynchronous code here
    newUser = User.User(32323)
    print(newUser)
    res = await newUser.createMessage('hello')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
