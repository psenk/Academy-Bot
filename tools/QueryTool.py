import json
import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv

from utils import Functions

load_dotenv(override=True)

#CONNECTION_STRING = os.getenv('PG_CONNECTION_STRING')
CONNECTION_STRING = "postgresql://postgres:postgres@localhost:5432/academy-test"

"""
JSON VOTE OBJECT
{
    "name": {
        "user": "Kyanize",
        "id": 912674589162518623
    },
    "vote": true,
    "comments": "blah blah blah",
    "timestamp": "05-05-2015T05:05:05PM"
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

    async def create_voting_period(self, title: str, nominee: str, comments: str, members: list, length: int) -> None:
        """
        
        """        
        query = 'INSERT INTO active_voting_periods (title, nominee, comments, member_ids, voted_ids, votes, start_date, length) VALUES ($1, $2, $3, $4, $5, $6, $7, $8);'
        self.logger.info(f'Create voting period query -> {query}')
        await self.execute(query, title, nominee, comments, members, [], [], datetime.now(), length)

    async def get_current_voting_period(self, id) -> list:
        """
        Get specific current voting period.
        return: list containing single voting period
        """
        query ='SELECT * FROM active_voting_periods WHERE id = $1;'
        voting_period = await self.fetch(query, id)
        self.logger.info('Single current voting period retrieved.')
        return voting_period
    
    async def get_past_voting_period(self, id) -> list:
        """
        Get specific past voting period.
        return: list containing single voting period
        """
        query = 'SELECT * FROM past_votes WHERE id = $1;'
        voting_period = await self.fetch(query, id)
        self.logger.info('Single past voting period retrieved.')
        return voting_period
    
    async def get_all_current_voting_periods(self) -> list:
        """
        Get all current voting periods.
        return: list of voting periods
        """
        query = 'SELECT * FROM active_voting_periods;'
        voting_periods = await self.fetch(query)
        self.logger.info('All current voting periods retrieved.')
        return voting_periods
    
    async def get_all_past_voting_periods(self) -> list:
        """
        Get all past voting periods.
        return: list of voting periods
        """
        query = 'SELECT * FROM past_voting_periods;'
        voting_periods = await self.fetch(query)
        self.logger.info('All past voting periods retrieved.')
        return voting_periods
    
    async def get_vote(self) -> list:
        pass

    async def delete_current_voting_period(self, id: int) -> None:
        """
        Delete current voting period from database.  Past must be deleted manually.
        param id: int - id # of period
        return: None
        """
        query = 'DELETE FROM active_voting_periods WHERE id = $1;'
        self.logger.info(f'Delete voting period query -> {query}')
        self.logger.info(f'--ID number -> {id}')
        await self.execute(query, id)
        self.logger.info('Voting period deleted.')

    async def submit_vote(self, vote: json, id: int) -> None:
        """
        Submit vote to specific period in database.
        param vote: json - vote object
        param id: int - id # of period
        return: None
        """
        query = 'UPDATE active_voting_periods SET votes = votes || $1::jsonb WHERE id = $2;'
        self.logger.info(f'Submit vote query -> {query}')
        self.logger.info(f'--JSON -> {vote}')
        self.logger.info(f'--ID number -> {id}')
        await self.execute(query, vote, id)
        data = json.loads(vote)
        await self.update_voted(data['name']['id'], id)
        self.logger.info('Vote submitted.')

    async def delete_vote(self, id: int, name: str) -> None:
        """
        Deletes specific vote.
        param id: int - id # of period
        param name: str - name of voter
        return: None
        """
        query = """
        WITH updated_votes AS (
            SELECT id, array_remove(votes, elem) AS new_votes
            FROM active_voting_periods, unnest(votes) AS elem
            WHERE id = $1 AND elem->'vote'->>'name' = $2
            )
        UPDATE active_voting_periods
        SET votes = updated_votes.new_votes
        FROM updated_votes
        WHERE active_voting_periods.id = updated_votes.id;
        """
        self.logger.info(f'Delete vote query -> {query}')
        self.logger.info(f'--ID number -> {id}')
        self.logger.info(f'--Name -> {name}')
        await self.execute(query, id, name)
        self.logger.info('Vote deleted.')

    async def update_voted(self, member_id: int, period_id: int) -> None:
        """
        Adds voter id to voted list.
        param member_id: int, id number of member
        param period_id: int, id of voting period
        return: None
        """
        query = 'UPDATE active_voting_periods SET voted_ids = voted_ids || $1::BIGINT[] WHERE id = $2;'
        self.logger.info(f'Update voted query -> {query}')
        self.logger.info(f'--Member ID -> {member_id}')
        self.logger.info(f'--Period ID -> {period_id}')
        await self.execute(query, [member_id], period_id)
        self.logger.info('Voted list updated.')
        
    async def get_voted(self, id: int) -> list:
        """
        Gets list of voters from period.
        param id: int, id of voting period
        return: list of voters
        """
        query = 'SELECT voted FROM active_voting_periods WHERE id = $1;'
        self.logger.info(f'Update voted query -> {query}')
        self.logger.info(f'--ID -> {id}')