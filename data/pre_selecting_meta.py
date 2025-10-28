# pre_selecting_meta.py (正确版本)
import pandas as pd
import os

print("Loading tracks.csv...")
tracks = pd.read_csv(
    '/Users/prism/musicagent/fma_metadata/tracks.csv', 
    header=[0, 1],           # 两级列名
    index_col=0,             # 第一列作为索引（track_id）
    low_memory=False
)

print(f"Original shape: {tracks.shape}")
print(f"Index name: {tracks.index.name}")  # 应该是 'track_id'
print(f"First 5 track IDs: {tracks.index[:5].tolist()}")

# 构建 DataFrame（track_id 从索引提取）
df = pd.DataFrame({
    'track_id': tracks.index,                      # 从索引获取
    'title': tracks[('track', 'title')],
    'artist': tracks[('artist', 'name')],
    'genre': tracks[('track', 'genre_top')],
    'duration': tracks[('track', 'duration')],
    'subset': tracks[('set', 'subset')]
})

print("\n" + "="*60)
print("Data preview:")
print("="*60)
print(df.head())

print("\n" + "="*60)
print("Cleaning data...")
print("="*60)

# 数据清洗
df = df.dropna(subset=['genre', 'duration'])
df['track_id'] = df['track_id'].astype(int)

# 过滤条件
df = df[(df['duration'] >= 30) & (df['duration'] <= 600)]  # 30秒~10分钟
df = df[df['genre'] != '']  # 去掉空 genre
df = df[df['artist'].notna()]  # 去掉空 artist

print(f"Total valid tracks: {len(df)}")

# 统计各风格数量
genre_counts = df['genre'].value_counts()
print("\n" + "="*60)
print("Top genres:")
print("="*60)
print(genre_counts.head(15))

# 分层抽样：确保风格多样性
print("\n" + "="*60)
print("Performing stratified sampling...")
print("="*60)

TARGET_SIZE = 10000
min_per_genre = 50  # 每个风格至少 50 首（调整为更合理的数量）
sampled_list = []
remaining = TARGET_SIZE

for genre, count in genre_counts.items():
    if remaining <= 0:
        break
    
    # 按比例分配，但确保每类至少有 min_per_genre
    ideal_n = int((count / len(df)) * TARGET_SIZE)
    n = min(count, max(min_per_genre, ideal_n), remaining)
    
    genre_subset = df[df['genre'] == genre]
    if len(genre_subset) >= n:
        sampled = genre_subset.sample(n=int(n), random_state=42)
        sampled_list.append(sampled)
        remaining -= n
        print(f"  {genre:20s}: sampled {n:4d} / {count:5d} available")

# 合并结果
final_df = pd.concat(sampled_list, ignore_index=True)

print("\n" + "="*60)
print(f"Final dataset size: {len(final_df)}")
print("="*60)
print("\nGenre distribution:")
print(final_df['genre'].value_counts())

# 保存到 data/ 目录
output_path = '/Users/prism/musicagent/data/fma_metadata.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

final_df = final_df[['track_id', 'title', 'artist', 'genre', 'duration']]
final_df.to_csv(output_path, index=False)

print("\n" + "="*60)
print(f"✅ Saved to {output_path}")
print("="*60)
print("\nSample rows:")
print(final_df.head(10))