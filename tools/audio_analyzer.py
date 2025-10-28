import pandas as pd
import os
from typing import Dict, Optional

class AudioAnalyzer:
    def __init__(self, metadata_path: str = "data/fma_metadata.csv"):
        """加载 FMA 元数据"""
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        self.df = pd.read_csv(metadata_path)
        self.df['track_id'] = self.df['track_id'].astype(int)
        self._track_dict = self.df.set_index('track_id').to_dict('index')
        print(f"✅ Loaded {len(self._track_dict)} tracks from {metadata_path}")

    def analyze(self, track_id: int) -> Optional[Dict]:
        if track_id not in self._track_dict:
            return None
        
        meta = self._track_dict[track_id]
        return {
            "genre": meta["genre"],
            "artist": meta["artist"],
            "title": meta["title"],
            "duration": float(meta["duration"])
        }

if __name__ == "__main__":
    analyzer = AudioAnalyzer()
    result = analyzer.analyze(104691)
    print("Analysis result:", result)