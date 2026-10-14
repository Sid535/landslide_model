import asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from landslide_backend.database import engine
from landslide_backend.models.db import RiskZone, Resource, Shelter  # noqa: F401 (registers models)


async def init_database():
    try:
        # Run Alembic migrations up to head — this replaces create_all()
        alembic_cfg = Config("alembic.ini")  # adjust path if run from elsewhere
        command.upgrade(alembic_cfg, "head")
        print("✅ Migrations applied (head)")

        # List tables, for a quick sanity check
        async with engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            print("\n📋 Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")

        print("\n🎉 Database initialization complete!")

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_database())
