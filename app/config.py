class Constants:
    __PASSWORD: str = (
        "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )
    __INITIAL_BALANCE: int = 1000
    __TOTAL_USERS: int = 50

    @classmethod
    def PASSWORD(cls) -> str:
        return cls.__PASSWORD

    @classmethod
    def INITIAL_BALANCE(cls) -> int:
        return cls.__INITIAL_BALANCE

    @classmethod
    def TOTAL_USERS(cls) -> int:
        return cls.__TOTAL_USERS
