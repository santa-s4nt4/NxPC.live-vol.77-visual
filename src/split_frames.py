import os
import shutil
import subprocess

# ==========================================
# 1. 設定
# ==========================================
target_extensions = ('.mov', '.mp4')

# 対象ファイルを取得し名前順にソート
video_files = sorted([
    f for f in os.listdir('.') 
    if os.path.isfile(f) and f.lower().endswith(target_extensions)
])

# すべての出力結果をまとめる親フォルダ（デスクトップなどに変更可能です）
main_output_dir = "FILM_Chunks"
frames_per_chunk = 100

if not video_files:
    print("❌ エラー: 対象となる動画ファイル（mp4, mov）が見つかりません。")
    exit()

print(f"📂 対象動画: {len(video_files)}本 ({', '.join(video_files)})\n")

# 親フォルダの作成
os.makedirs(main_output_dir, exist_ok=True)

# ==========================================
# 2. 動画ごとの個別処理ループ
# ==========================================
for video_file in video_files:
    # ファイル名から拡張子を取り除く（例: "a.mov" -> "a"）
    video_name = os.path.splitext(video_file)[0]
    
    print(f"========== [{video_file}] の処理を開始 ==========")
    
    # この動画専用の作業フォルダとZIP保存フォルダを設定
    temp_frames_dir = f"temp_frames_{video_name}"
    video_chunks_dir = os.path.join(main_output_dir, video_name)
    
    # フォルダの初期化
    if os.path.exists(temp_frames_dir): shutil.rmtree(temp_frames_dir)
    if os.path.exists(video_chunks_dir): shutil.rmtree(video_chunks_dir)
    os.makedirs(temp_frames_dir, exist_ok=True)
    os.makedirs(video_chunks_dir, exist_ok=True)

    # ------------------------------------------
    # ① ffmpegでフレーム抽出
    # ------------------------------------------
    print(f"🎬 1. {video_name} のフレームを抽出中...")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_file, 
        "-vf", "fps=5", 
        f"{temp_frames_dir}/%05d.png"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # 抽出したPNGファイルを取得
    all_frames = sorted([
        os.path.join(temp_frames_dir, f) for f in os.listdir(temp_frames_dir) if f.endswith('.png')
    ])
    
    # ------------------------------------------
    # ② チャンク分割とZIP圧縮
    # ------------------------------------------
    print(f"📁 2. {video_name} を分割・ZIP圧縮中...")
    chunk_index = 1
    
    for i in range(0, len(all_frames), frames_per_chunk):
        chunk_name = f"chunk_{chunk_index:03d}"
        chunk_path = os.path.join(video_chunks_dir, chunk_name)
        os.makedirs(chunk_path, exist_ok=True)

        # オーバーラップ（+1枚）処理
        chunk_files = all_frames[i : i + frames_per_chunk + 1]

        for f in chunk_files:
            shutil.copy(f, chunk_path)
        
        # ZIP化して元の生フォルダを削除
        shutil.make_archive(chunk_path, 'zip', chunk_path)
        shutil.rmtree(chunk_path)

        chunk_index += 1

    # 作業が終わった一時フォルダ(temp_frames_a など)を削除してストレージを節約
    shutil.rmtree(temp_frames_dir)
    print(f"✅ [{video_file}] 完了！ -> '{video_chunks_dir}/' に保存されました。\n")

print(f"🎉 すべての動画の処理が完了しました！\n親フォルダ '{main_output_dir}' を確認してください。")