# API server for online-chip system

### Running

* Host: `0.0.0.0`
* Port: `8080`

```bash
poetry run gunicorn --config setting.py
```

If you run this program first time, you need to run `poetry install` first.

To clone this repository without permitted account, add **deploy key**.

### API list

API URL: [https://shikosai.mtaisei.com/api](https://shikosai.mtaisei.com/api)

| Path | Request Method | Function |
| --- | --- | --- |
| `/balance/{user_id}` | `GET` |  Get `user`'s current balance |
| `/inc/` | `PUT` | Increase or Decrease `user`'s balance |

Response Data format: `{ user_id: int, balance: int }`
