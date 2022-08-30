#python native
from uuid import UUID
from datetime import datetime
from typing import Optional

#pydantic
from pydantic import (
    BaseModel,
    Field
)

#user module
from .user import User

class TweetBase(BaseModel):
    tweet_id: UUID  = Field(
        ...,
        title="Tweet ID",
        description="It is the id of the tweet"
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Content",
        description="It is the content of the tweet",
        example="It's a tweet"
    )

    by: User = Field(
        ...,
        title="User info",
        description="It is the information of the user who created the tweet"
    )

class UpdateTweet(TweetBase):
    updated_at: Optional[datetime] = Field(
        default=None,
        title="Update date",
        description="It is the date of the last time the tweet was updated"
    )

class Tweet(UpdateTweet):
    created_at: Optional[datetime] = Field(
        default=None,
        title="Creation date",
        description="Is the date when the tweet was created"
    )