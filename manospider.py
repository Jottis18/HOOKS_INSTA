import os
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ColorClip
from PIL import Image

# Corrigir uso de ANTIALIAS para versões mais novas do Pillow
Image.ANTIALIAS = Image.LANCZOS

def criar_videos_com_hooks_da_pasta(video_principal_path, pasta_hooks, duracao_imagem=5, output_dir="C:\\Users\\paulo\\Desktop\\output"):
    os.makedirs(output_dir, exist_ok=True)

    # Lista arquivos .mp4 apenas na pasta indicada, sem subpastas
    hooks_paths = [
        os.path.join(pasta_hooks, f)
        for f in os.listdir(pasta_hooks)
        if f.lower().endswith(".mp4")
    ]

    if not hooks_paths:
        print("❌ Nenhum arquivo .mp4 encontrado na pasta.")
        return

    for i, hook_path in enumerate(hooks_paths):
        print(f"🔧 Processando hook {i+1}: {os.path.basename(hook_path)}")

        # Abrir os vídeos individualmente em cada loop
        video_principal = VideoFileClip(video_principal_path)
        hook_clip = VideoFileClip(hook_path).resize(newsize=(video_principal.w, video_principal.h))

        # Concatenar o hook e o vídeo principal
        video_completo = concatenate_videoclips([hook_clip, video_principal])

        # Criar uma faixa verde (100px de altura) na parte inferior


        # Salvar o vídeo
        nome_hook = os.path.splitext(os.path.basename(hook_path))[0]
        saida_path = os.path.join(output_dir, f"video_final_{i+1}_{nome_hook}.mp4")
        video_completo.write_videofile(saida_path, codec="libx264", audio_codec="aac")

        # Fechar os clipes para liberar recursos
        video_completo.close()
        video_completo.close()
        hook_clip.close()
        video_principal.close()

        time.sleep(2)

    print("✅ Todos os vídeos foram gerados.")

# === USO REAL COM SEUS CAMINHOS ===
video_principal = r"C:\Users\paulo\Downloads\d1b729b407254b178828099b170c8681.MP4"
pasta_hooks = r"C:\Users\paulo\Downloads\videos"
duracao_logo = 5  # segundos

criar_videos_com_hooks_da_pasta(video_principal, pasta_hooks, duracao_imagem=duracao_logo)
