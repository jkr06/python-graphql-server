import asyncio
from ariadne import ObjectType, SubscriptionType
from graphql import GraphQLResolveInfo
from typing import Any

USERS = [
  {
    "username": "john",
    "name": "john doe",
    "status": "ACTIVE",
    "email": "johndoe@mail.com"
  },
  {
    "username": "xyz",
    "name": "xyz ABC",
    "status": "INACTIVE",
    "email": "xyz@mail.com"
  },
  {
    "username": "123",
    "name": "123 788",
    "status": "BANNED",
    "email": "123555@mail.com"
  }
]

query = ObjectType("Query")
mutation = ObjectType("Mutation")
subscription = SubscriptionType()
types = [query, mutation, subscription]

@query.field("user")
async def user(obj: Any, info: GraphQLResolveInfo,
    username: str, status: str):
  return next((user for user in USERS
    if user["username"] == username and
      user["status"] == status), {})

@mutation.field("add_user")
async def add_user(obj, info: GraphQLResolveInfo, username: str,
    name: str, email: str):
  USERS.append({
    "username": username,
    "name": name,
    "status": "ACTIVE",
    "email": email
  })
  return {"status": "ACTIVE"}

@subscription.source("users")
async def users_generator(obj, info):
  for user in USERS:
      await asyncio.sleep(1)
      yield user

@subscription.field("users")
def users_resolver(user, info):
    return user


