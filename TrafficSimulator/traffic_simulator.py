import aiohttp
from aiohttp import web

def action_generator():
    pass

def exploit_injector():
    pass

def user_simulator():
    pass

async def handle(request):
    async with aiohttp.ClientSession() as session:
        async with session.get(request.rel_url) as resp:
            return web.Response(body=await resp.read())

app = web.Application()
app.router.add_route('*', '/{tail:.*}', handle)
web.run_app(app, port=8080)