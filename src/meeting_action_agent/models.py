"""
Shared Pydantic data models for the Meeting-to-Action Agent.

These models define the expected structure of the agent's extracted meeting data,
including decisions, action items, open questions, risks, supporting evidence,
and validation results.
"""

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


class Risk(BaseModel):
    """
    A risk, blocker, uncertainty, or possible problem identified in the meeting.
    """

    risk: str = Field(
        description="The identified risk."
    )
    status: InformationStatus = Field(
        description="Whether the risk was explicit, inferred, or unclear."
    )
    evidence: list[EvidenceItem] = Field(
        default_factory=list,
        description="Meeting text evidence supporting the risk."
    )


class MeetingExtraction(BaseModel):
    """
    Top-level data model for the agent's extracted meeting output.

    This model defines the expected structure of the complete output from one
    meeting transcript or notes file.
    """

    meeting_title: str = Field(
        default="Untitled meeting",
        description="Short descriptive title for the meeting."
    )
    summary: str = Field(
        description="Brief summary of the meeting."
    )
    decisions: list[Decision] = Field(
        default_factory=list,
        description="Decisions identified in the meeting."
    )
    action_items: list[ActionItem] = Field(
        default_factory=list,
        description="Action items identified in the meeting."
    )
    open_questions: list[OpenQuestion] = Field(
        default_factory=list,
        description="Open questions identified in the meeting."
    )
    risks: list[Risk] = Field(
        default_factory=list,
        description="Risks identified in the meeting."
    )


class ValidationResult(BaseModel):
    """
    Result returned by the deterministic validation tool.
    """

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)