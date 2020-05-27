from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
import uvicorn

from resolvers.swapi import types as swapi_types
from resolvers.user import types as user_types

type_defs = load_schema_from_path("./schema")
schema = make_executable_schema(type_defs, *[swapi_types, user_types])

async def homepage(request):
    return PlainTextResponse("Homepage")


app = Starlette()
app.add_route("/", homepage)
app.mount("/graphql", GraphQL(schema))

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")

