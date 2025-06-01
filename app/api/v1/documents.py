from fastapi import APIRouter, Depends, HTTPException, Query, status
from uuid import UUID
from app.controllers.document_controller import DocumentController
from app.repositories.library_repo import LibraryRepository
from app.schemas.document import DocumentCreate, DocumentResponse
from app.schemas.chunk import ChunkCreate, ChunkResponse
from app.utils.response import sendResponse

router = APIRouter(prefix="/documents", tags=["Documents"])

def get_document_controller() -> DocumentController:
    return DocumentController(LibraryRepository())

@router.post("/create", response_model=DocumentResponse)
def create_document(payload: DocumentCreate, controller: DocumentController = Depends(get_document_controller)):
    try:
        document = controller.add_document(payload.library_id, payload.dict())
        return sendResponse(status.HTTP_201_CREATED, "Document created", document.dict())
    
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: UUID, library_id: UUID = Query(...), controller: DocumentController = Depends(get_document_controller)):
    try:
        document = controller.get_document(library_id, document_id)
        return sendResponse(status.HTTP_200_OK, "Document retrieved", document.dict())
    
    except ValueError as e:
        return sendResponse(status.HTTP_404_NOT_FOUND, str(e))


@router.post("/{document_id}/chunks", response_model=ChunkResponse)
def add_chunk(library_id: UUID, document_id: UUID, payload: ChunkCreate, controller: DocumentController = Depends(get_document_controller)):
    
    try:
        chunk = controller.add_chunk(library_id, document_id, payload.dict())
        return sendResponse(status.HTTP_201_CREATED, "Chunk added to document", chunk.dict())
    
    except ValueError as e:
        return sendResponse(status.HTTP_400_BAD_REQUEST, str(e))
    

def delete_chunk(document_id: UUID, chunk_id: UUID, library_id: UUID = Query(...), controller: DocumentController = Depends(get_document_controller)):
    
    try:
        controller.delete_chunk(library_id, document_id, chunk_id)
        return sendResponse(status.HTTP_200_OK, "Chunk deleted", None)
    
    except ValueError as e:
        return sendResponse(status.HTTP_404_NOT_FOUND, str(e))
