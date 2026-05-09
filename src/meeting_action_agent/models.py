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


class ActionItem(BaseModel):
    """
    A follow-up task identified in the meeting.
    """

    task: str = Field(
        description="The action item or task to complete."
    )
    owner: str = Field(
        description="The person responsible for the task. Use 'Unclear' if missing."
    )
    deadline: str = Field(
        description="The deadline for the task. Use 'Not specified' if missing."
    )
    context: str = Field(
        description="Short explanation of why this task exists."
    )
    status: InformationStatus = Field(
        description="Whether the task was explicit, inferred, or unclear."
    )
    evidence: list[EvidenceItem] = Field(
        default_factory=list,
        description="Meeting text evidence supporting the action item."
    )


class OpenQuestion(BaseModel):
    """
    An unresolved question from the meeting.
    """

    question: str = Field(
        description="The unresolved question."
    )
    status: InformationStatus = Field(
        description="Whether the question was explicit, inferred, or unclear."
    )
    evidence: list[EvidenceItem] = Field(
        default_factory=list,
        description="Meeting text evidence supporting the open question."
    )