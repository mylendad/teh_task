from pydantic import BaseModel, ConfigDict, HttpUrl


class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    pass


class URLUpdate(URLBase):
    pass


class URLInfo(URLBase):
    code: str

    model_config = ConfigDict(
        from_attributes=True,  # позволяет Pydantic напрямую сопоставлять атрибуты этих объектов sqlite3.Row с полями схемы Pydantic, без необходимости предварительного преобразования   █
        # объекта sqlite3.Row в словарь. Это делает процесс более эффективным и удобным.
        populate_by_name=True,
    )
