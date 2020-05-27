import asyncio
from ariadne import ObjectType
from graphql import GraphQLResolveInfo
import httpx
from typing import Any

query = ObjectType("Query")
people = ObjectType("StarWarPeople")
types = [query, people]

@query.field("swapi_people")
async def swapi_people(obj: Any, info: GraphQLResolveInfo,
    person: str):
  async with httpx.AsyncClient() as client:
    response = await client.get(f"https://swapi.dev/api/people/?search={person}")
    print(response.json())
    return response.json()["results"]

@people.field("vehicles")
async def swapi_vehicles(person, info: GraphQLResolveInfo):
  async with httpx.AsyncClient() as client:
    response = await asyncio.gather(*[
      client.get(vehicle) for vehicle in person["vehicles"]])
    return [r.json() for r in response]

@people.field("films")
async def swapi_films(person, info: GraphQLResolveInfo):
  async with httpx.AsyncClient() as client:
    response = await asyncio.gather(*[
      client.get(film) for film in person["films"]])
    return [r.json() for r in response]

@people.field("starships")
async def swapi_starships(person, info: GraphQLResolveInfo):
  async with httpx.AsyncClient() as client:
    response = await asyncio.gather(*[
      client.get(starship) for starship in person["starships"]])
    return [r.json() for r in response]

