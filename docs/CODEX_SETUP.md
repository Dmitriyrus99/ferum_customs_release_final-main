# Установка и настройка Codex

Этот документ описывает процесс установки [Codex CLI](https://github.com/openai/codex) на сервере или в другой среде, где развёрнуто приложение.

## Установка

Codex распространяется через npm, поэтому предварительно требуется Node.js. Затем выполните:

```bash
npm install -g @openai/codex
```

Проверить корректность установки можно командой `codex --help`.

## Базовая конфигурация

Codex ищет настройки в каталоге `~/.codex/`. Создайте там файл `config.yaml` со следующим содержимым:

```yaml
model: o4-mini
approvalMode: suggest
fullAutoErrorMode: ask-user
notify: true
providers:
  - name: OpenAI
    baseURL: https://api.openai.com/v1
    envKey: OPENAI_API_KEY
```

API‑ключ необходимо передать через переменную окружения:

```bash
export OPENAI_API_KEY="<ваш-ключ>"
```

При желании можно подключить другие провайдеры или изменить модель.

После этого запускайте `codex` в каталоге проекта. CLI предложит дальнейшие действия.
