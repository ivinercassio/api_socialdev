# Documentação do Projeto: SOCIAL.DEV

## Mapeamento do Banco de Dados

### Tabelas e Atributos

* **USER:** `{ INT id, STRING username, STRING password, BOOLEAN public, STRING about, TYPE type, DATE creation_date }`
* **POST:** `{ INT id, STRING title, STRING legend, INT author (USER), INT like, DATETIME date_published }`
* **MIDEA:** `{ INT id, INT owner (USER), INT post (POST), BOOLEAN image_profile, BLOB file, STRING LINK }`
* **TAG:** `{ INT id, STRING theme }`
* **POST_TAG:** `{ INT id, INT tag (TAG), INT post (POST) }`
* **FRIEND:** `{ INT id, INT friend_one (USER), INT friend_two (USER), DATE date_start }`
* **MESSAGE:** `{ INT id, INT friend (FRIEND), INT from (USER), INT to (USER), STRING text, DATETIME data_published }`
* **COMMENT:** `{ INT id, STRING text, INT post (POST), INT owner (USER), DATETIME date_publisheded }`
* **REPORT:** `{ INT id, INT post (POST), INT comment (COMMENT), DATETIME date_report }`

---

## Mapeamento dos Endpoints da API

* CRUD PADRÃO PARA TODAS AS ENTIDADES

### Endpoints Customizados

#### `GET /api/posts/:id/user`
Retorna uma lista com todos os posts de um usuário (ex.: visualização de um feed de perfil).

#### `GET /api/post_tags/:id/tag`
Retorna uma lista com todos os posts de uma tag.

#### `GET /api/post_tags/:id/post`
Retorna uma lista com todas as tags de um post.

#### `GET /api/mideas/:id/post`
Retorna uma lista com todas as mídias de um post.

#### `GET /api/mideas/:id/user`
Retorna a imagem de perfil de um usuário (`this.owner != null && this.image_profile == TRUE`).

#### `GET /api/friends/:id/user`
Retorna uma lista com todos os usuários que são amigos de outro usuário.

#### `GET /api/messages/:id/friend`
Retorna uma lista com todas as mensagens entre dois amigos.

#### `GET /api/comments/:id/post`
Retorna uma lista com todos os comentários de um post.

#### `GET /api/reports/:id/post`
Retorna uma lista com todas as denúncias de um post.

### `GET /api/reports/:id/comment`
Retorna uma lista com todas as denúncias de um comment.

---

## Para iniciar o projeto:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata seed_data.json
python manage.py runserver
```