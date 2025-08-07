from common.config import LLM_API, LLM_API_KEY, LLM_MODEL
from schema.schema import AssessmentRequest, AssessmentResult
from services.llmmanager import LLMManeger


class AssesmentAgent:
    """
    Assessment Agent for generating and managing assessments.

    This agent handles the creation, validation, and management of assessments,
    including questions, answer keys, and results.
    """

    def __init__(self):
        self.llm = LLMManeger(LLM_MODEL, LLM_API_KEY, LLM_API)

    def invoke(self, request: AssessmentRequest) -> AssessmentResult:
        """
        Generate an assessment based on the provided request parameters.

        Args:
            request (AssessmentRequest): The parameters for generating the assessment.

        Returns:
            AssessmentResult: The generated assessment result.
        """
        # Validate the request
        if not isinstance(request, AssessmentRequest):
            raise ValueError("Invalid request type")

        # Call LLM to generate assessment
        response = self.llm.create_assessment(request)

        # Parse and return the assessment result
        return response
