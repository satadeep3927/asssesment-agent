from datetime import datetime

import pandas as pd
import streamlit as st

from agents.assementagent import AssesmentAgent
from schema.schema import (
    AssessmentRequest,
    AssessmentResult,
    BloomsTaxonomyLevel,
    DifficultyLevel,
)


def initialize_session_state():
    """Initialize session state variables"""
    if "assessment_history" not in st.session_state:
        st.session_state.assessment_history = []
    if "current_assessment" not in st.session_state:
        st.session_state.current_assessment = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "📝 Generate Assessment"


def display_assessment_form():
    """Display the assessment configuration form"""
    st.header("🎯 Assessment Generator")
    st.markdown("Configure your assessment parameters below:")

    col1, col2 = st.columns(2)

    with col1:
        curriculum_standard = st.text_input(
            "Curriculum Standard",
            value="CBSE Class 10",
            help="e.g., CBSE Class 10, IB MYP, Common Core Grade 8",
        )

        learning_objectives = st.text_area(
            "Learning Objectives",
            value="Understanding quadratic equations and their applications",
            height=100,
            help="Specific learning goals and outcomes",
        )

        blooms_level = st.selectbox(
            "Bloom's Taxonomy Level",
            options=[level.value for level in BloomsTaxonomyLevel],
            index=1,
            help="Cognitive level to target",
        )

        difficulty = st.selectbox(
            "Difficulty Level",
            options=[level.value for level in DifficultyLevel],
            index=1,
            help="Overall difficulty of the assessment",
        )

    with col2:
        total_marks = st.number_input(
            "Total Marks",
            min_value=1,
            max_value=1000,
            value=50,
            help="Total marks for the entire assessment",
        )

        number_of_questions = st.number_input(
            "Number of Questions",
            min_value=1,
            max_value=50,
            value=5,
            help="Total number of questions to generate",
        )

        additional_prompts = st.text_area(
            "Additional Requirements",
            placeholder="e.g., Include real-world applications, Focus on problem-solving",
            height=100,
            help="Any additional requirements or constraints",
        )

    # Question Distribution
    st.subheader("📊 Question Distribution")
    dist_col1, dist_col2, dist_col3 = st.columns(3)

    with dist_col1:
        mcq_percentage = st.slider(
            "MCQ Percentage",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.1,
            format="%.1f",
        )

    with dist_col2:
        short_answer_percentage = st.slider(
            "Short Answer Percentage",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            format="%.1f",
        )

    with dist_col3:
        long_answer_percentage = st.slider(
            "Long Answer Percentage",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            format="%.1f",
        )

    # Validation for percentages
    total_percentage = mcq_percentage + short_answer_percentage + long_answer_percentage
    if abs(total_percentage - 1.0) > 0.01:
        st.warning(
            f"⚠️ Question type percentages should sum to 1.0 (current: {total_percentage:.2f})"
        )

    # Generate button
    if st.button("🚀 Generate Assessment", type="primary", use_container_width=True):
        if total_percentage <= 1.01:  # Allow small floating point errors
            with st.spinner("Generating assessment... This may take a few moments."):
                try:
                    # Create assessment request
                    request = AssessmentRequest(
                        curriculum_standard=curriculum_standard,
                        learning_objectives=learning_objectives,
                        blooms_taxonomy_level=BloomsTaxonomyLevel(blooms_level),
                        toughness_level=DifficultyLevel(difficulty),
                        total_marks=total_marks,
                        number_of_questions=number_of_questions,
                        additional_prompts=(
                            additional_prompts if additional_prompts else None
                        ),
                        mcq_percentage=mcq_percentage,
                        short_answer_percentage=short_answer_percentage,
                        long_answer_percentage=long_answer_percentage,
                    )

                    # Generate assessment
                    agent = AssesmentAgent()
                    result = agent.invoke(request)

                    # Store in session state
                    st.session_state.current_assessment = result

                    # Add to history
                    st.session_state.assessment_history.append(
                        {
                            "timestamp": datetime.now(),
                            "title": result.title,
                            "curriculum": curriculum_standard,
                            "questions": len(result.questions),
                            "marks": total_marks,
                            "result": result,
                        }
                    )

                    st.success("✅ Assessment generated successfully!")
                    
                    # Auto-navigate to results page
                    st.session_state.current_page = "📋 View Current Assessment"
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error generating assessment: {str(e)}")
        else:
            st.error("❌ Please ensure question type percentages sum to 1.0")


def display_assessment_result(assessment: AssessmentResult):
    """Display the generated assessment"""
    st.header("📋 Generated Assessment")

    # Assessment Info
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Title:** {assessment.title}")
        st.info(f"**Curriculum:** {assessment.curriculum_standard}")
        st.info(f"**Learning Objectives:** {assessment.learning_objectives}")

    with col2:
        st.info(f"**Total Questions:** {assessment.metadata.total_questions}")
        st.info(f"**Total Marks:** {assessment.metadata.total_marks}")
        st.info(f"**Target Level:** {assessment.target_blooms_level.title()}")

    if assessment.description:
        st.markdown(f"**Description:** {assessment.description}")

    # Instructions
    st.subheader("📝 Student Instructions")
    st.markdown(assessment.student_instructions)

    if assessment.teacher_notes:
        st.subheader("👨‍🏫 Teacher Notes")
        st.markdown(assessment.teacher_notes)

    # Questions
    st.subheader("❓ Questions")

    for i, question in enumerate(assessment.questions, 1):
        with st.expander(
            f"Question {i} ({question.question_type.replace('_', ' ').title()}) - {question.marks} marks"
        ):
            st.markdown(f"**Question:** {question.question_text}")

            # Display options for MCQ
            if question.options:
                st.markdown("**Options:**")
                for option in question.options:
                    correct_marker = "✅" if option.is_correct else "❌"
                    st.markdown(f"- {option.option_id}: {option.text} {correct_marker}")

            # Answer Key
            if question.answer_key:
                st.markdown("**Answer Key:**")
                if question.answer_key.correct_answer:
                    if isinstance(question.answer_key.correct_answer, list):
                        st.markdown(
                            f"- **Correct Answer:** {', '.join(question.answer_key.correct_answer)}"
                        )
                    else:
                        st.markdown(
                            f"- **Correct Answer:** {question.answer_key.correct_answer}"
                        )

                if question.answer_key.explanation:
                    st.markdown(f"- **Explanation:** {question.answer_key.explanation}")

                if question.answer_key.marking_criteria:
                    st.markdown(
                        f"- **Marking Criteria:** {question.answer_key.marking_criteria}"
                    )

                if question.answer_key.key_points:
                    st.markdown("- **Key Points:**")
                    for point in question.answer_key.key_points:
                        st.markdown(f"  - {point}")

            # Metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"Difficulty: {question.difficulty.title()}")
            with col2:
                st.caption(f"Bloom's Level: {question.blooms_level.title()}")
            with col3:
                if question.estimated_time_minutes:
                    st.caption(f"Est. Time: {question.estimated_time_minutes} min")

    # Assessment Metadata
    st.subheader("📊 Assessment Statistics")

    col1, col2 = st.columns(2)

    with col1:
        # Difficulty Distribution
        st.markdown("**Difficulty Distribution:**")
        if assessment.metadata.difficulty_distribution:
            df_difficulty = pd.DataFrame(
                list(assessment.metadata.difficulty_distribution.items()),
                columns=["Difficulty", "Count"],
            )
            st.bar_chart(df_difficulty.set_index("Difficulty"))

    with col2:
        # Question Type Distribution
        st.markdown("**Question Type Distribution:**")
        if assessment.metadata.question_type_distribution:
            df_types = pd.DataFrame(
                list(assessment.metadata.question_type_distribution.items()),
                columns=["Type", "Count"],
            )
            df_types["Type"] = df_types["Type"].str.replace("_", " ").str.title()
            st.bar_chart(df_types.set_index("Type"))

    # Export Options
    st.subheader("💾 Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        # JSON Export
        json_data = assessment.model_dump_json(indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_data,
            file_name=f"assessment_{assessment.title.replace(' ', '_').lower()}.json",
            mime="application/json",
        )

    with col2:
        # Text Export
        text_export = generate_text_export(assessment)
        st.download_button(
            label="📝 Download Text",
            data=text_export,
            file_name=f"assessment_{assessment.title.replace(' ', '_').lower()}.txt",
            mime="text/plain",
        )

    with col3:
        if st.button("🔄 Generate New Assessment"):
            st.session_state.current_assessment = None
            st.session_state.current_page = "📝 Generate Assessment"
            st.rerun()


def generate_text_export(assessment: AssessmentResult) -> str:
    """Generate a text export of the assessment"""
    lines = []
    lines.append(f"ASSESSMENT: {assessment.title}")
    lines.append("=" * 50)
    lines.append(f"Curriculum Standard: {assessment.curriculum_standard}")
    lines.append(f"Learning Objectives: {assessment.learning_objectives}")
    lines.append(f"Total Questions: {assessment.metadata.total_questions}")
    lines.append(f"Total Marks: {assessment.metadata.total_marks}")
    lines.append("")

    lines.append("STUDENT INSTRUCTIONS:")
    lines.append("-" * 20)
    lines.append(assessment.student_instructions)
    lines.append("")

    lines.append("QUESTIONS:")
    lines.append("-" * 10)

    for i, question in enumerate(assessment.questions, 1):
        lines.append(f"\nQ{i}. {question.question_text} [{question.marks} marks]")

        if question.options:
            for option in question.options:
                lines.append(f"   {option.option_id}. {option.text}")

        lines.append("")

    lines.append("\nANSWER KEY:")
    lines.append("-" * 11)

    for i, question in enumerate(assessment.questions, 1):
        lines.append(f"\nQ{i} Answer:")
        if question.answer_key and question.answer_key.correct_answer:
            if isinstance(question.answer_key.correct_answer, list):
                lines.append(f"   {', '.join(question.answer_key.correct_answer)}")
            else:
                lines.append(f"   {question.answer_key.correct_answer}")

        if question.answer_key and question.answer_key.explanation:
            lines.append(f"   Explanation: {question.answer_key.explanation}")

    return "\n".join(lines)


def display_assessment_history():
    """Display assessment history"""
    st.header("📚 Assessment History")

    if not st.session_state.assessment_history:
        st.info("No assessments generated yet.")
        return

    for i, entry in enumerate(reversed(st.session_state.assessment_history)):
        with st.expander(
            f"{entry['title']} - {entry['timestamp'].strftime('%Y-%m-%d %H:%M')}"
        ):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Questions", entry["questions"])
            with col2:
                st.metric("Total Marks", entry["marks"])
            with col3:
                st.metric("Curriculum", entry["curriculum"])
            with col4:
                if st.button(
                    "View Details",
                    key=f"view_{len(st.session_state.assessment_history)-i}",
                ):
                    st.session_state.current_assessment = entry["result"]
                    st.session_state.current_page = "📋 View Current Assessment"
                    st.rerun()


def main():
    st.set_page_config(
        page_title="AI Assessment Generator",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("🎯 AI Assessment Generator")
    st.markdown("Generate comprehensive assessments with AI-powered question creation")

    # Initialize session state
    initialize_session_state()

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Page",
            [
                "📝 Generate Assessment",
                "📋 View Current Assessment",
                "📚 Assessment History",
            ],
            index=0 if st.session_state.current_page == "📝 Generate Assessment" 
                  else 1 if st.session_state.current_page == "📋 View Current Assessment"
                  else 2,
        )
        
        # Update current page in session state
        st.session_state.current_page = page

        st.divider()
        st.markdown("### About")
        st.markdown(
            """
            This app uses AI to generate comprehensive assessments based on:
            - Curriculum standards
            - Learning objectives  
            - Bloom's taxonomy levels
            - Difficulty preferences
            - Question type distribution
            """
        )

    # Main content based on selected page
    if page == "📝 Generate Assessment":
        display_assessment_form()

    elif page == "📋 View Current Assessment":
        if st.session_state.current_assessment:
            display_assessment_result(st.session_state.current_assessment)
        else:
            st.info("No assessment generated yet. Please generate an assessment first.")
            if st.button("🚀 Generate Assessment"):
                st.session_state.current_page = "📝 Generate Assessment"
                st.rerun()

    elif page == "📚 Assessment History":
        display_assessment_history()

    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <p>AI Assessment Generator | Powered by Advanced Language Models</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
