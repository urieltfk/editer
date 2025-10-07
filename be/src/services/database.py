from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional
import logging
from ..settings import settings
from ..models.document import Document

logger = logging.getLogger(__name__)


class DatabaseManager:
    """MongoDB database connection manager with Beanie ODM."""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.initialized: bool = False
    
    async def connect(self) -> None:
        """Initialize Beanie with MongoDB connection."""
        try:
            # Create Motor client
            self.client = AsyncIOMotorClient(
                settings.mongodb_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection
            await self.client.admin.command('ping')
            
            # Initialize Beanie
            await init_beanie(
                database=self.client[settings.database_name],
                document_models=[Document]
            )
            
            self.initialized = True
            logger.info(f"Beanie initialized with MongoDB: {settings.database_name}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionError(f"Database connection failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected database error: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self.initialized = False
            logger.info("Disconnected from MongoDB")
    
    async def health_check(self) -> bool:
        """Check if database connection is healthy."""
        try:
            if not self.client or not self.initialized:
                return False
            await self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()
