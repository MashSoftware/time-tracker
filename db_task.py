import os

import psycopg2

# Connect to an existing database
conn = psycopg2.connect(os.environ.get("DATABASE_URL"))

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command
cur.execute("delete from event where started_at < now() - interval '3 months';")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()
