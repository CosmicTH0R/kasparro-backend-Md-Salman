import uuid
import hashlib
import requests # Needed for real APIs
import pandas as pd # Needed for CSV
import io
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.database import SessionLocal
from src.core.models import RawDataAPI, RawDataCSV, UnifiedData, ETLJob
from src.schemas.data import UnifiedRecord

class ETLPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.run_id = str(uuid.uuid4())
        # TODO: PASTE YOUR REAL KEY HERE
        self.COINPAPRIKA_KEY = "YOUR_COINPAPRIKA_KEY_HERE" 

    def generate_hash(self, *args):
        text = "".join(str(a) for a in args)
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def run(self):
        job = ETLJob(run_id=self.run_id, status="running", start_time=datetime.now())
        self.db.add(job)
        self.db.commit()
        
        try:
            print(f"--- Starting ETL Run: {self.run_id} ---")
            
            # 1. CoinPaprika (API Source 1)
            self._fetch_coinpaprika()
            
            # 2. CoinGecko (API Source 2 - P1 Requirement)
            self._fetch_coingecko()
            
            # 3. CSV Source (P0 Requirement)
            self._fetch_local_csv()
            
            job.status = "success"
            job.end_time = datetime.now()
            self.db.commit()
            print("--- ETL Run Completed Successfully ---")
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.end_time = datetime.now()
            self.db.commit()
            print(f"!!! ETL Failed: {e}")

    def _upsert_unified(self, source, original_id, title, content, price, date_obj):
        """Helper to save clean data to DB"""
        # Create a unique hash based on ID and Price (so we detect price changes)
        data_hash = self.generate_hash(source, original_id, price, date_obj)
        
        exists = self.db.query(UnifiedData).filter_by(data_hash=data_hash).first()
        if not exists:
            unified = UnifiedData(
                source_type=source,
                original_id=str(original_id),
                title=title,
                content=f"{content} | Price: ${price}", # Storing price in content for simplicity
                published_date=date_obj or datetime.now(),
                data_hash=data_hash
            )
            self.db.add(unified)

    def _fetch_coinpaprika(self):
        print("Fetching CoinPaprika (Public Mode)...")
        # Ensure we use the exact endpoint format from the docs you pasted
        url = "https://api.coinpaprika.com/v1/tickers" 
        
        try:
            # We remove the 'Authorization' header completely because the docs say "no signup"
            response = requests.get(url) 
            
            if response.status_code == 200:
                # We limit to top 5 to avoid processing too much data
                data = response.json()[:5] 
                
                # A. Save Raw
                raw = RawDataAPI(raw_payload={"source": "coinpaprika", "data": data})
                self.db.add(raw)
                
                # B. Normalize
                for coin in data:
                    self._upsert_unified(
                        source="CoinPaprika",
                        original_id=coin['id'],
                        title=coin['name'],
                        content=f"Rank: {coin['rank']}",
                        price=coin['quotes']['USD']['price'],
                        date_obj=datetime.now()
                    )
                self.db.commit()
                print("CoinPaprika Fetch Success!")
            else:
                print(f"CoinPaprika Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"CoinPaprika Exception: {e}")
    def _fetch_coingecko(self):
        print("Fetching CoinGecko...")
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                # A. Save Raw
                raw = RawDataAPI(raw_payload={"source": "coingecko", "data": data})
                self.db.add(raw)
                
                # B. Normalize
                for coin in data:
                    self._upsert_unified(
                        source="CoinGecko",
                        original_id=coin['id'],
                        title=coin['name'],
                        content=f"Symbol: {coin['symbol']}",
                        price=coin['current_price'],
                        date_obj=datetime.now()
                    )
                self.db.commit()
            else:
                print(f"CoinGecko Error: {response.status_code}")
        except Exception as e:
            print(f"CoinGecko Exception: {e}")

    def _fetch_local_csv(self):
        print("Processing Local CSV File...")
        try:
            # FIX: Read from the actual file system, not a hardcoded string
            file_path = "data/legacy.csv"
            
            # Check if file exists to avoid crashing
            import os
            if not os.path.exists(file_path):
                print(f"Warning: {file_path} not found. Skipping CSV source.")
                return

            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                # A. Save Raw
                raw = RawDataCSV(raw_row_content=row.to_dict())
                self.db.add(raw)
                
                # B. Normalize
                self._upsert_unified(
                    source="LegacyCSV",
                    original_id=str(row['id']),
                    title=str(row['coin']),
                    content="Legacy Data Archive",
                    price=float(row['price']),
                    date_obj=datetime.now()
                )
            self.db.commit()
            print("CSV Ingestion Complete.")
            
        except Exception as e:
            print(f"CSV Ingestion Failed: {e}")
if __name__ == "__main__":
    db = SessionLocal()
    pipeline = ETLPipeline(db)
    pipeline.run()
    db.close()