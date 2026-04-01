from neo4j import GraphDatabase

uri = "neo4j+s://a9b028d2.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("a9b028d2", "OObuKomgvhbnHhw7YbxPiZqTLRI1LCF7mLnjbUUGDco"))

try:
    driver.verify_connectivity()
    print("✅ Connected successfully!")
except Exception as e:
    print(f"❌ Failed: {e}")
finally:
    driver.close()