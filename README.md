# Transcritor

Transcritor de áudio local (Whisper na GPU) e download de vídeo do YouTube em MP3.

- `Transcritor.exe` — janela para transcrever áudio (usa `src/worker.py`).
- `youtube.py` — baixa o áudio de links do YouTube em MP3 (yt-dlp) e transcreve.
- `src/` — código-fonte da janela (`Transcritor.cs`, `build.ps1`) e o `worker.py` do Whisper.
- `skills/transcrever-youtube/` — skill do Claude Code que roda `youtube.py` a partir de um link.

## Requisitos

Python com `openai-whisper`, `torch` (CUDA) e `yt-dlp`; ffmpeg no PATH. Os caminhos assumem
`E:\Transcritor` e `C:\Python314\python.exe`; ajuste se mudar de lugar.

## Uso

```
python youtube.py "URL" [URL2 ...] [--idioma pt] [--modelo turbo] [--pasta nome]
```

Saída em `videos/<pasta>/` com o `.mp3` e o `.txt` lado a lado. Para usar a skill, copie
`skills/transcrever-youtube` para `~/.claude/skills/`.
