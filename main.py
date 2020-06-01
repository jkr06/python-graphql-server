from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
import uvicorn

from resolvers.swapi import types as swapi_types
from resolvers.user import types as user_types

type_defs = load_schema_from_path("./schema")
schema = make_executable_schema(type_defs, *[swapi_types, user_types])

async def homepage(request):
    return PlainTextResponse("Welcome. Open /graphql for the graphql playground")

class BackgroundTaskMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # set request.state.background to BackgroundTask instance in resolver
        response = await call_next(request)
        if hasattr(request.state, 'background'):
            response.background = request.state.background
        return response


middleware = [
    Middleware(BackgroundTaskMiddleware)
]


app = Starlette(middleware=middleware)
app.add_route("/", homepage)
app.mount("/graphql", GraphQL(schema))

# This method can be used as well
# @app.middleware("http")
# async def dispatch(request: Request, call_next: RequestResponseEndpoint) -> Response:
#     response = await call_next(request)
#     if hasattr(request.state, 'background'):
#         response.background = request.state.background
#     return response


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")

