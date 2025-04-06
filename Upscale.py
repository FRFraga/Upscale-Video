import os
import subprocess
import multiprocessing
from pathlib import Path
import shutil
import time
from tqdm import tqdm

# ====== Configurações iniciais ======
video_path = r"C:\Users\nando\OneDrive\Documentos\Upscale\meuvideo.mp4"
frames_dir = "frames"
output_dir = "out"
final_video = "video_final.mp4"
temp_video = "video_temp_sem_audio.mp4"
realesrgan_path = r"C:\Users\nando\Real-ESRGAN\realesrgan-ncnn-vulkan-v0.2.0-windows\realesrgan-ncnn-vulkan.exe"
model_name = "realesrgan-x4plus-anime"

# ====== Utilitários ======
def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        tqdm.write(f"❌ Erro ao executar: {cmd}")
        raise e

# ====== Etapas do pipeline ======
def extrair_frames(video_path, frames_dir):
    os.makedirs(frames_dir, exist_ok=True)
    cmd = f'ffmpeg -i "{video_path}" {frames_dir}/frame_%05d.png -loglevel quiet'
    run_cmd(cmd)

def processar_frame(args):
    frame, output_dir, realesrgan_path, model_name = args
    output_file = Path(output_dir) / Path(frame).name
    cmd = f'"{realesrgan_path}" -i "{frame}" -o "{output_file}" -n {model_name}'
    run_cmd(cmd)
    return True

def compilar_video_sem_audio(output_dir, temp_video):
    cmd = f'ffmpeg -framerate 30 -i {output_dir}/frame_%05d.png -c:v libx264 -pix_fmt yuv420p "{temp_video}" -loglevel quiet'
    run_cmd(cmd)

def adicionar_audio(original_video, temp_video, final_video):
    cmd = f'ffmpeg -i "{temp_video}" -i "{original_video}" -c copy -map 0:v:0 -map 1:a:0 -shortest "{final_video}" -loglevel quiet'
    run_cmd(cmd)

def renomear_frames(output_dir):
    output_files = sorted(Path(output_dir).glob("*.png"))
    for i, f in enumerate(tqdm(output_files, desc="🔄 Renomeando frames")):
        novo_nome = Path(output_dir) / f"frame_{i:05d}.png"
        f.rename(novo_nome)

# ====== Benchmark refinado ======
def benchmark_realesrgan(frames, realesrgan_path, output_dir, model_name, num_processes):
    args = [(f, output_dir, realesrgan_path, model_name) for f in frames]
    start = time.time()
    with multiprocessing.Pool(num_processes) as pool:
        for _ in tqdm(pool.imap_unordered(processar_frame, args),
                      total=len(frames),
                      desc=f"🔍 Teste com {num_processes} processos", leave=False):
            pass
    return time.time() - start

def encontrar_melhor_num_processes(frames, realesrgan_path, output_dir, model_name):
    resultados = {}
    valores_para_testar = [1, 2, 3, 4, 5, 6]
    amostra = frames[:min(10, len(frames))]  # usa até 10 frames para benchmark

    tqdm.write("⏱️ Iniciando benchmark de paralelismo...")
    for n in valores_para_testar:
        shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir)
        tempo = benchmark_realesrgan(amostra, realesrgan_path, output_dir, model_name, n)
        resultados[n] = tempo

    melhor = min(resultados, key=resultados.get)
    tqdm.write(f"🏁 Melhor configuração: {melhor} processo(s) ({resultados[melhor]:.2f} segundos)")
    return melhor

# ====== Execução principal ======
if __name__ == "__main__":
    # Limpa e recria pastas
    for d in [frames_dir, output_dir]:
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)

    # Etapa 1: Extração
    extrair_frames(video_path, frames_dir)

    # Lista todos os frames
    all_frames = sorted(str(f) for f in Path(frames_dir).glob("*.png"))

    # Etapa 2: Benchmark automático
    num_processes = encontrar_melhor_num_processes(all_frames, realesrgan_path, output_dir, model_name)

    # Etapa 3: Processamento completo com melhor paralelismo
    args = [(f, output_dir, realesrgan_path, model_name) for f in all_frames]
    with multiprocessing.Pool(num_processes) as pool:
        with tqdm(total=len(all_frames), desc="✨ Processando frames em alta qualidade") as pbar:
            for _ in pool.imap_unordered(processar_frame, args):
                pbar.update(1)

    # Etapa 4: Renomeia para garantir ordem
    renomear_frames(output_dir)

    # Etapa 5: Compila sem áudio
    compilar_video_sem_audio(output_dir, temp_video)

    # Etapa 6: Junta com o áudio original
    adicionar_audio(video_path, temp_video, final_video)

    tqdm.write(f"✅ Processo finalizado com sucesso! Vídeo salvo como: {final_video}")
