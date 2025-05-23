from flask import Flask, request, render_template, redirect, url_for
import os
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image

Image.ANTIALIAS = Image.LANCZOS

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def criar_videos_com_hooks_da_pasta(video_principal_path, pasta_hooks, duracao_imagem=5):
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

        video_principal = VideoFileClip(video_principal_path)
        hook_clip = VideoFileClip(hook_path).resize(newsize=(video_principal.w, video_principal.h))
        video_completo = concatenate_videoclips([hook_clip, video_principal])

        nome_hook = os.path.splitext(os.path.basename(hook_path))[0]
        saida_path = os.path.join(OUTPUT_FOLDER, f"video_final_{i+1}_{nome_hook}.mp4")
        video_completo.write_videofile(saida_path, codec="libx264", audio_codec="aac")

        video_completo.close()
        hook_clip.close()
        video_principal.close()

        time.sleep(2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video = request.files['video']
        hooks = request.files.getlist('hooks')

        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)

        hooks_folder = os.path.join(UPLOAD_FOLDER, 'hooks')
        os.makedirs(hooks_folder, exist_ok=True)

        for hook in hooks:
            hook.save(os.path.join(hooks_folder, hook.filename))

        criar_videos_com_hooks_da_pasta(video_path, hooks_folder)
        return "✅ Vídeos processados com sucesso!"

    return '''
        <h2>Gerar vídeos com hooks</h2>
        <form method="POST" enctype="multipart/form-data">
            Vídeo principal: <input type="file" name="video"><br><br>
            Hooks (.mp4 múltiplos): <input type="file" name="hooks" multiple><br><br>
            <input type="submit" value="Processar">
        </form>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
