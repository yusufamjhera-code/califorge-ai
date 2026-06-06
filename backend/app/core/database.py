"""
Async MongoDB connection management using Motor.

Provides a singleton database client with connection pooling,
health checks, and graceful startup/shutdown lifecycle.
"""

from __future__ import annotations

import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class Database:
    """Async MongoDB connection manager.

    Usage:
        db = Database()
        await db.connect()
        collection = db.get_collection("users")
        await db.disconnect()
    """

    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls) -> None:
        """Establish MongoDB connection with connection pooling."""
        settings = get_settings()
        try:
            cls._client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
                maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
            )
            cls._database = cls._client[settings.MONGODB_DATABASE]

            # Verify connection with a ping
            await cls._client.admin.command("ping")
            logger.info(
                "✅ Connected to MongoDB: %s (database: %s)",
                settings.MONGODB_URI,
                settings.MONGODB_DATABASE,
            )

            # Create indexes
            await cls._create_indexes()
        except Exception as exc:
            logger.error("❌ Failed to connect to MongoDB: %s", exc)
            raise

    @classmethod
    async def disconnect(cls) -> None:
        """Gracefully close the MongoDB connection."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._database = None
            logger.info("🔌 Disconnected from MongoDB")

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Return the active database instance.

        Raises:
            RuntimeError: If the database connection has not been established.
        """
        if cls._database is None:
            raise RuntimeError(
                "Database not initialized. Call Database.connect() first."
            )
        return cls._database

    @classmethod
    def get_collection(cls, name: str):
        """Return a specific collection from the active database.

        Args:
            name: The name of the MongoDB collection.

        Returns:
            An AsyncIOMotorCollection instance.
        """
        return cls.get_database()[name]

    @classmethod
    async def health_check(cls) -> dict:
        """Perform a database health check.

        Returns:
            A dict with status and server info.
        """
        try:
            info = await cls._client.admin.command("ping")
            return {"status": "healthy", "ping": info}
        except Exception as exc:
            return {"status": "unhealthy", "error": str(exc)}

    @classmethod
    async def _create_indexes(cls) -> None:
        """Create required database indexes for optimal query performance."""
        db = cls.get_database()

        # Users collection
        await db.users.create_index("firebase_uid", unique=True)
        await db.users.create_index("email", unique=True, sparse=True)

        # Assessments collection
        await db.assessments.create_index("user_id")
        await db.assessments.create_index([("user_id", 1), ("created_at", -1)])

        # Fitness scores collection
        await db.fitness_scores.create_index("user_id")
        await db.fitness_scores.create_index(
            [("user_id", 1), ("calculated_at", -1)]
        )

        # Workout plans collection
        await db.workout_plans.create_index("user_id")
        await db.workout_plans.create_index(
            [("user_id", 1), ("is_active", 1)]
        )

        # Progress / weight entries
        await db.weight_entries.create_index(
            [("user_id", 1), ("recorded_at", -1)]
        )

        # Workout logs
        await db.workout_logs.create_index(
            [("user_id", 1), ("completed_at", -1)]
        )

        # Achievements
        await db.achievements.create_index("user_id")

        logger.info("📇 Database indexes created successfully")
