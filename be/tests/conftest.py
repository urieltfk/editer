"""
Pytest configuration and shared fixtures.
"""
import os

os.environ["DEBUG"] = "False"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017"
os.environ["DATABASE_NAME"] = "test_editer"
os.environ["HRID_SEED"] = "test-seed-for-testing-123"
