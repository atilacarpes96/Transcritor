# Addon: o Transcritor te ajuda a lembrar do que foi falado

Quer que o Transcritor não só transcreva, mas guarde o que cada vídeo ensinou e te lembre
quando aparecer o mesmo problema? Use este addon.

Cada vídeo estudado vira um arquivo curto em `aprendizados\` (ideia central, lições, o que você
aplicou, quando lembrar). O `INDICE.md` liga **problema → vídeo → solução**. A pasta fica fora
do git porque é pessoal.

## 1. Preparar (uma vez)

```bash
python aprendizados.py iniciar
```

Copie a skill para a sua conta do Claude Code (ela já traz o passo 4, "guarde o ensinamento"):

```bash
cp -r skills/transcrever-youtube ~/.claude/skills/
```

E coloque no `CLAUDE.md` da pasta onde você trabalha (ou em `~/.claude/CLAUDE.md`):

```markdown
- Base de ensinamentos dos vídeos: `<caminho do Transcritor>\aprendizados\INDICE.md`
  (problema → vídeo → solução). Ler antes de responder um problema que um vídeo possa ter resolvido.
```

## 2. Usar conversando com o Claude

| Você diz | O que acontece |
|---|---|
| "transcreve e aprende: <link>" | transcreve, resume e cria o arquivo em `aprendizados\` com as linhas no índice |
| "aquele vídeo que falava de X" | o Claude procura no índice e nas transcrições |
| "tô com o problema Y" | ele confere o índice antes de responder e cita o vídeo |
| "já aplicamos o que o vídeo Z ensinou" | ele atualiza o "O que aplicamos" do vídeo |

## 3. Comandos (sem o Claude)

```bash
python aprendizados.py novo "assunto do video" --url https://youtu.be/... --titulo "Título"
```

```bash
python aprendizados.py listar
```

```bash
python aprendizados.py buscar cache cota
```

O `buscar` procura todos os termos (sem ligar para acento) nos aprendizados e em todas as
transcrições de `videos\`, e mostra arquivo e linha.

## Arquivos do addon

- `aprendizados.py`: os comandos acima.
- `aprendizados-modelo\MODELO.md` e `INDICE.md`: modelos usados pelo `novo` e pelo `iniciar`.
- `skills\transcrever-youtube\SKILL.md`: passo 4 guarda o ensinamento.
