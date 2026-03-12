from codesage.config_db.neo4j_db_conn import Neo4jClient


def main() -> None:
    client = Neo4jClient()
    try:
        client.verify()
        rows = client.execute_query("RETURN 'Neo4j connected' AS message")
        print("connection test:", rows)

        # clears db
        client.execute_query("MATCH (n) DETACH DELETE n")
        print("cleared database")
        
        # Create sample nodes
        client.execute_query(
            """
                CREATE (a:Person {name: $name})
                CREATE (b:Person {name: $friendName})
                CREATE (a)-[:KNOWS]->(b)
            """,
            {"name": "code", "friendName": "sage"}
        )
        print("created Person nodes and KNOWS relationship")

        result = client.execute_query(
            "MATCH (p:Person) RETURN p.name AS name"
        )
        print("people in database:", result)
        
    finally:
        client.close()


if __name__ == "__main__":
    main()