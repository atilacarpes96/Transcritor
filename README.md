# Transcritor

Transcritor de áudio local (Whisper turbo na GPU) e download de vídeo do YouTube, TikTok e Instagram em MP3 (qualquer site do yt-dlp).

**Para que serve:** transformar em texto uma gravação, uma reunião ou um vídeo do YouTube/TikTok/Instagram, no seu PC,
sem enviar o áudio para a internet (só o download do próprio vídeo usa a rede).

**Como funciona:** a janela (`Transcritor.exe`) recebe arquivos de áudio/vídeo ou um link; para links,
o `yt-dlp` baixa o áudio em MP3; o `src/worker.py` roda o Whisper na placa de vídeo e grava o `.txt`
ao lado do áudio. A skill `transcrever-youtube` permite pedir isso ao Claude Code só com o link.

- `Transcritor.exe` — janela para transcrever áudio (usa `src/worker.py`). Aceita arquivos ou um link do YouTube: cole o link e clique em "Baixar e transcrever" (MP3 e .txt ficam em `videos/<título>/` ao lado do exe).
- `youtube.py` — baixa o áudio de links do YouTube em MP3 (yt-dlp) e transcreve.
- `src/` — código-fonte da janela (`Transcritor.cs`, `build.ps1`) e o `worker.py` do Whisper.
- `skills/transcrever-youtube/` — skill do Claude Code que roda `youtube.py` a partir de um link.

## Requisitos

Placa de vídeo **NVIDIA** com o driver instalado (o Whisper roda na GPU). Python com `openai-whisper`, `torch` (CUDA) e `yt-dlp[default,curl-cffi]` (o `curl-cffi` é necessário para o TikTok); ffmpeg no PATH.

Para instalar tudo de uma vez, dê dois cliques em `INSTALAR.bat`: ele confere a placa NVIDIA, instala Python, ffmpeg e as bibliotecas, baixa o modelo turbo, compila o `Transcritor.exe` e cria o atalho. Se você já tem um Python com essas bibliotecas, aponte a variável de ambiente `TRANSCRITOR_PYTHON` para ele e o instalador o reaproveita.

Se a placa tiver pouca memória e o modelo não couber, o `worker.py` continua no processador em vez de falhar (mais devagar).

## Créditos

Suporte a TikTok, Instagram e outros sites do yt-dlp, instalador automático e queda para o processador quando falta memória na placa: [Thiago](https://github.com/Thiagos97) (fork [Thiagos97/Transcritor](https://github.com/Thiagos97/Transcritor)).

## Uso

```
python youtube.py "URL" [URL2 ...] [--idioma pt] [--pasta nome]
```

Para Instagram (e vídeos que pedem login), salve um `cookies.txt` do navegador na pasta do programa; ele é usado automaticamente e nunca vai para o git.

Saída em `videos/<site>/<título>/` (ou `videos/<pasta>/` com `--pasta`) com o `.mp3` e o `.txt` lado a lado. Para usar a skill, copie
`skills/transcrever-youtube` para `~/.claude/skills/`.



## Addon: aprendizados

Para o Transcritor guardar o que cada vídeo ensinou e te lembrar quando o problema voltar,
veja [ADDON-APRENDIZADOS.md](ADDON-APRENDIZADOS.md) (`python aprendizados.py iniciar | novo | listar | buscar`).
