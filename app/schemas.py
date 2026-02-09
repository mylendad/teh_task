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
        from_attributes=True,
        populate_by_name=True,
    )
