from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.controllers.library_controller import LibraryController
from app.repositories.library_repo import LibraryRepository
from app.schemas.library import LibraryCreate, LibraryResponse
from app.utils.response import sendResponse

router = APIRouter(prefix="/libraries", tags=["Libraries"])

def get_library_controller() -> LibraryController:
    return LibraryController(LibraryRepository())

@router.post("/create", response_model = LibraryResponse)
def create_library(payload: LibraryCreate, controller: LibraryController = Depends(get_library_controller)):
    try:
        library = controller.create_library(name=payload.name, metadata=payload.metadata)
        return sendResponse(status.HTTP_201_CREATED, "Library created", library.dict())
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/get/{library_id}", response_model = LibraryResponse)
def get_library(library_id: UUID, controller: LibraryController = Depends(get_library_controller)):
    try:
        library = controller.get_library(library_id)
        return sendResponse(status.HTTP_200_OK, "Library retrieved", library.dict())
    
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/get", response_model= list[LibraryResponse])
def list_libraries(controller: LibraryController = Depends(get_library_controller)):
    try:
        libraries = controller.list_libraries()
        return sendResponse(
            status_code=status.HTTP_200_OK,
            message="Libraries retrieved successfully",
            body=[lib.dict() for lib in libraries]
        )
    
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))


@router.delete("/delete/{library_id}")
def delete_library(library_id: UUID, controller: LibraryController = Depends(get_library_controller)):
    try:
        controller.delete_library(library_id)
        return sendResponse(status.HTTP_200_OK, "Library deleted successfully")
    
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))


@router.put("/update/{library_id}", response_model=LibraryResponse)
def update_library(library_id: UUID, payload: LibraryCreate, controller: LibraryController = Depends(get_library_controller)):
    try:
        updated_library = controller.update_library(library_id, name=payload.name, metadata=payload.metadata)
        return sendResponse(status.HTTP_200_OK, "Library updated successfully", updated_library.dict())
    
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))

