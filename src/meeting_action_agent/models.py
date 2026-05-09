from typing import Literal
from pydantic import BaseModel, Field


InformationStatus = Literal["explicit", "inferred", "unclear"]


class EvidenceItem(BaseModel):
    """
    A short text snippet from the meeting input that supports an extracted item
    such as a decision, action item, open question, or risk.
    """

    quote: str = Field(
        description="A direct quote or close snippet from the meeting text."
    )


class Decision(BaseModel):
    """
    A decision that is identified and agreed on in the meeting.
    """

    decision: str = Field(
        description="The decision that was made."
    )
    status: InformationStatus = Field(
        description="Whether the decision was explicit, inferred, or unclear."
    )
    evidence: list[EvidenceItem] = Field(
        default_factory=list,
        description="Meeting text evidence supporting the decision."
    )
