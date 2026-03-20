import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import Any
from neo4j.exceptions import Neo4jError

load_dotenv()

class Neo4jClient:
    def __init__(self) -> None:
        """init environment variables and connect to Neo4j database."""
        conn_str=os.getenv("NEO4J_URI")
        user=os.getenv("NEO4J_USER")
        password=os.getenv("NEO4J_PASSWORD")

        assert conn_str is not None, "NEO4J_URI is not set in environment variables"
        assert user is not None, "NEO4J_USER is not set in environment variables"
        assert password is not None, "NEO4J_PASSWORD is not set in environment variables"

        self.driver = GraphDatabase.driver(conn_str, auth=(user, password))

    def verify(self) -> None:
        """verifies the connection to neo4j db"""
        self.driver.verify_connectivity()

    def close(self) -> None:
        """closes the connection with neo4j db"""
        self.driver.close()
    
    def execute_query(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """executes a cypher query and returns the results."""
        with self.driver.session() as session:
            try:
                result = session.run(query, params) # pyright: ignore[reportArgumentType]
                return [record.data() for record in result]
            except Neo4jError as e:
                print(f"Error executing query: {e}")
                return []
            
    