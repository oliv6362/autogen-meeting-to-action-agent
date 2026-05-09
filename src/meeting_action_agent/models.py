from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    """
    A short text snippet from the meeting input that supports an extracted item
    such as a decision, action item, open question, or risk.
    """

    quote: str = Field(
        description="A direct quote or close snippet from the meeting text."
    )


