"""
db.py

Database layer for ClaimPulse.
Connects to MongoDB if available via MONGODB_URI in .env.
Automatically falls back to local file-backed storage if MongoDB is unavailable
so the enterprise portal operates seamlessly in any environment.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_DB_FILE = REPO_ROOT / "api" / "local_storage.json"

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.use_mongo = False
        
        mongo_uri = os.getenv("MONGODB_URI", "").strip()
        if mongo_uri:
            try:
                import pymongo
                self.client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=1500)
                # Test connection
                self.client.admin.command('ping')
                self.db = self.client.get_database()
                self.use_mongo = True
                logger.info("Successfully connected to MongoDB.")
            except Exception as e:
                logger.warning(f"MongoDB connection failed ({e}). Using local file persistence.")
                self.use_mongo = False
        else:
            logger.info("No MONGODB_URI provided. Using local file persistence.")
            
        self._init_local_storage()

    def _init_local_storage(self):
        if not LOCAL_DB_FILE.exists():
            default_data = {
                "users": [
                    {
                        "username": "adjuster@claimpulse.io",
                        "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # password: admin
                        "role": "adjuster",
                        "full_name": "Senior Claims Adjudicator"
                    },
                    {
                        "username": "policyholder@claimpulse.io",
                        "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # password: admin
                        "role": "policyholder",
                        "full_name": "Alex Morgan"
                    }
                ],
                "claims": []
            }
            LOCAL_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
            LOCAL_DB_FILE.write_text(json.dumps(default_data, indent=2), encoding="utf-8")

    def _read_local(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            if not LOCAL_DB_FILE.exists():
                self._init_local_storage()
            return json.loads(LOCAL_DB_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"users": [], "claims": []}

    def _write_local(self, data: Dict[str, List[Dict[str, Any]]]):
        LOCAL_DB_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # User operations
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        if self.use_mongo and self.db is not None:
            return self.db.users.find_one({"username": username}, {"_id": 0})
        data = self._read_local()
        for u in data.get("users", []):
            if u["username"] == username:
                return u
        return None

    def create_user(self, user_doc: Dict[str, Any]) -> bool:
        if self.get_user(user_doc["username"]):
            return False
        doc_to_save = dict(user_doc)
        if self.use_mongo and self.db is not None:
            self.db.users.insert_one(doc_to_save)
            return True
        data = self._read_local()
        data.setdefault("users", []).append(doc_to_save)
        self._write_local(data)
        return True

    # Claim operations
    def insert_claim(self, claim_doc: Dict[str, Any]) -> str:
        doc_to_save = dict(claim_doc)
        if self.use_mongo and self.db is not None:
            self.db.claims.insert_one(doc_to_save)
            return claim_doc.get("claim_id", "")
        data = self._read_local()
        data.setdefault("claims", []).append(doc_to_save)
        self._write_local(data)
        return claim_doc.get("claim_id", "")


    def get_all_claims(self, role: str, username: str) -> List[Dict[str, Any]]:
        if self.use_mongo and self.db is not None:
            query = {"claim_id": {"$not": {"$regex": "^CP-SAMPLE-"}}}
            if role != "adjuster":
                query["submitted_by"] = username
            return list(self.db.claims.find(query, {"_id": 0}).sort("timestamp", -1))
        
        data = self._read_local()
        claims = [c for c in data.get("claims", []) if not str(c.get("claim_id", "")).startswith("CP-SAMPLE-")]
        if role != "adjuster":
            claims = [c for c in claims if c.get("submitted_by") == username]
        return sorted(claims, key=lambda x: x.get("timestamp", ""), reverse=True)


    def get_claim_by_id(self, claim_id: str) -> Optional[Dict[str, Any]]:
        if self.use_mongo and self.db is not None:
            return self.db.claims.find_one({"claim_id": claim_id}, {"_id": 0})
        data = self._read_local()
        for c in data.get("claims", []):
            if str(c.get("claim_id")) == str(claim_id):
                return c
        return None

db_manager = DatabaseManager()
