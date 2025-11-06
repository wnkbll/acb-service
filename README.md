# FastAPI backend application

## Как запустить

```
git clone https://github.com/wnkbll/acb-service.git
cd acb-service
``` 
Далее нужно заполнить `.env` файл.  
Проще всего переименовать `.env.example`, так как его содержимое подойдет для локального разворачивания сервиса.  

Для запуска контейнеров:
```
docker compose up
```

Для доступа к swagger документации сервиса нужно перейти по адресу `http://localhost:9999/docs`