from fastapi import APIRouter, Depends, status
from app.controllers.search_controller import SearchController
from app.repositories.library_repo import LibraryRepository
from app.schemas.search import SearchRequest, SearchResult
from app.utils.response import sendResponse

router = APIRouter(prefix="/search", tags=["Search"])

def get_search_controller() -> SearchController:
    return SearchController(LibraryRepository())

@router.post("/", response_model=list[SearchResult])
def search_chunks(request: SearchRequest, controller: SearchController = Depends(get_search_controller)):
    try:
        results = controller.search(request)
        return sendResponse(
            status_code=status.HTTP_200_OK,
            message=f"Top {len(results)} result(s) retrieved",
            body=[r.dict() for r in results]
        )
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))
