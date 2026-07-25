from api.database import (save_analysis,get_all_analyses, get_analysis_by_id,
delete_analysis,)


def create_analysis(request):
    """
    Save a generated AI analysis.
    """

    analysis_id = save_analysis(
        title=request.title,
        paper_arxiv_ids=request.paper_arxiv_ids,
        analysis_type=request.analysis_type,
        analysis_depth=request.analysis_depth,
        writing_style=request.writing_style,
        output_format=request.output_format,
        additional_instructions=request.additional_instructions,
        generated_markdown=request.generated_markdown,
    )

    return {
        "analysis_id": analysis_id,
        "message": "Analysis saved successfully."
    }

def fetch_all_analyses():
    return get_all_analyses()


def fetch_analysis(analysis_id):
    return get_analysis_by_id(analysis_id)


def remove_analysis(analysis_id):
    deleted = delete_analysis(analysis_id)

    return {
        "deleted": deleted
    }