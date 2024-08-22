import uuid
import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv

from utils import Functions

load_dotenv(override=True)

CONNECTION_STRING = os.getenv('PG_CONNECTION_STRING')


class QueryTool:
    def __init__(self) -> None:
        """
        QueryTool constructor
        return: None
        """
        self.logger = Functions.create_logger('tools')
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



    async def delete_submission(self, uuid_no: uuid.UUID) -> None:
        """
        Deletes submission from database.
        param uuid_no: str - UUID of task
        return: None
        """
        query = 'DELETE FROM submissions WHERE uuid_no = $1;'
        self.logger.info(f'Delete submission query -> {query}')
        self.logger.info(f'UUID number -> {uuid_no}')
        await self.execute(query, uuid_no)
        self.logger.info('Submission deleted.')
