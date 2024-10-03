# API server for online-chip system

### API list

API URL: [](https://shikosai.mtaisei.com/api)

| Path | Request Method | Function |
| --- | --- | --- |
| `/balance/{user_id}` | `GET` |  Get `user`'s current balance |
| `/inc/` | `PUT` | Increase or Decrease `user`'s balance |

Response Data format: `{ user_id: int, balance: int }`
