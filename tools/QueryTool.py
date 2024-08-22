import uuid
import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv

from utils import Functions

load_dotenv(override=True)

CONNECTION_STRING = os.getenv('PG_CONNECTION_STRING')

"""
JSON VOTE OBJECT
{
    "vote": {
        "name": "Kyanize",
        "vote": true,
        "comments": "blah blah blah",
        "timestamp": 05-05-2015T05:05:05PM
    }
}
"""


class QueryTool:
    def __init__(self) -> None:
        """
        QueryTool constructor
        return: None
        """
        self.logger = Functions.create_logger('querytool')
        self.pool = None

    async def __aenter__(self) -> 'QueryTool':
        """
        Initializes connection pool when entering context (with statement)
        return: QueryTool Class instance
        """
        self.pool = await asyncpg.create_pool(dsn=CONNECTION_STRING, min_size=2, max_size=10)
        self.logger.info('Connection pool created.')
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Closes connection pool when exiting context (with statement)
        return: None
        """
        await self.pool.close()
        self.logger.info('Connection pool closed.')

    async def execute(self, query: str, *args) -> None:
        """
        Executes a database query without returning results.
        param query: str - SQL query
        param args: arguments for the SQL query
        return: None
        """
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(query, *args)
            self.logger.info('Query executed successfully.')
        except Exception as e:
            self.logger.error(f'Query attempted -> {query}')
            self.logger.error(f'Error executing query -> {e}', exc_info=True)
            raise

    async def fetch(self, query: str, *args) -> list:
        """
        Executes a query and returns multiple rows.
        param query: str - SQL query
        param args: arguments for the SQL query
        return: list - rows returned by the query
        """
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetch(query, *args)
        except Exception as e:
            self.logger.error(f'Error fetching data -> {e}', exc_info=True)
            raise

    async def fetchval(self, query: str, *args) -> any:
        """
        Executes a query and returns a single value.
        param query: str - SQL query
        param args: arguments for the SQL query
        return: any - value returned by the query
        """
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetchval(query, *args)
        except Exception as e:
            self.logger.error(f'Error fetching value -> {e}', exc_info=True)
            raise

    async def create_voting_period(self) -> None:
        pass
    
    async def submit_vote(self) -> None:
        pass

    async def get_voting_period(self) -> list:
        pass
    
    async def get_vote(self) -> list:
        pass

    async def delete_voting_period(self, id: int) -> None:
        """
        Delete voting period from database.
        param id: int - id # of task
        return: None
        """
        query = 'DELETE FROM current_votes WHERE id = $1;'
        self.logger.info(f'Delete voting period query -> {query}')
        self.logger.info(f'--ID number -> {id}')
        await self.execute(query, id)
        self.logger.info('Voting period deleted.')

    async def delete_vote(self, id: int, name: str) -> None:
        """
        Deletes specific vote.
        param id: int - id # of period
        return: None
        """
        query = """
        WITH updated_votes AS (
            SELECT id, array_remove(votes, elem) AS new_votes
            FROM current_votes, unnest(votes) AS elem
            WHERE id = $1 AND elem->'vote'->>'name' = $2
            )
        UPDATE current_votes
        SET votes = updated_votes.new_votes
        FROM updated_votes
        WHERE current_votes.id = updated_votes.id;
        """
        self.logger.info(f'Delete vote query -> {query}')
        self.logger.info(f'--ID number -> {id}')
        self.logger.info(f'--Name -> {name}')
        await self.execute(query, id, name)
        self.logger.info('Vote deleted.')
