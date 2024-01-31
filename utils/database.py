import aiosqlite, json

class Database:
    connect: aiosqlite.Connection = None
    id: int

    def __init__(self, id):
        self.id = id
    
    async def bootstrap(self, file: str):
        if not self.connect:
            self.connect = await aiosqlite.connect(file)

        await self.connect.execute(f"""
            CREATE TABLE IF NOT EXISTS `{self.id}` (
            `mod`  TEXT        NOT NULL,
            `var`  TEXT UNIQUE NOT NULL,
            `val`              NOT NULL
        )
        """)

    async def set(self, module, variable, value):
        params = dict(mod=module, var=variable, val=json.dumps(value))
        if await (await self.connect.execute(f"SELECT 1 FROM `{self.id}` WHERE mod = :mod AND var = :var", params)
            ).fetchall() == []:
            await self.connect.execute(f"INSERT INTO `{self.id}` (mod, var, val) VALUES (:mod, :var, :val)", params)
        else:
            await self.connect.execute(f"UPDATE `{self.id}` SET val = :val WHERE mod = :mod AND var = :var ", params)

        await self.connect.commit()
    
    async def get(self, module, variable, default=None):
        c = await (await self.connect.execute(
            f"SELECT `val` FROM `{self.id}` WHERE `mod`=:mod AND `var`=:var",
            {'mod': module, 'var': variable}
        )).fetchall()
        if c == []:
            return default
        return json.loads(c[0][0])

    async def exec(self, sql) -> list | None:
        result = await (await self.connect.execute(sql)).fetchall()
        await self.connect.commit()
        return result

from typing import Any

class DictStorage(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set(self, __key: str, __value: Any) -> Any:
        self[__key] = __value