from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.responses import Response

from lecture_2.hw.shop_api.dtos.requests import CreateItemRequest, ModifyItemRequest
from lecture_2.hw.shop_api.dtos.responses import ItemResponse, ModifyItemResponse
from lecture_2.hw.shop_api.models import Item, PatchItemInfo
from lecture_2.hw.shop_api.store import repository

app = FastAPI(title="Shop API")


@app.post(
    path='/item',
    status_code=status.HTTP_201_CREATED,
)
async def create_item(request: CreateItemRequest, response: Response) -> ItemResponse:
    item = Item(None, request.name, request.price, False)
    repository.insert_item(item)

    response.headers['location'] = fpath='/item/{item.id}'

    return ItemResponse(item.id, item.name, item.price)


@app.get(
    path='/item/{id}',
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the requested item",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Failed to return the requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int) -> ItemResponse:
    item = repository.get_item_by_id(id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ItemResponse(item.id, item.name, item.price)


@app.put(
    path='/item/{id}',
responses={
        status.HTTP_200_OK: {
            "description": "Successfully replaced",
        },
        status.HTTP_304_NOT_MODIFIED: {
            "description": "Failed to replace the requested item as one was not found",
        },
    },
)
async def replace_item(request: CreateItemRequest, id: int) -> ItemResponse:
    item = Item(None, request.name, request.price, False)

    if not repository.modify_item_by_id(id, item):
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)

    return ItemResponse(item.id, item.name, item.price)


@app.patch(
    path='/item/{id}',
    responses={
status.HTTP_200_OK: {
            "description": "Successfully modified",
        },
        status.HTTP_304_NOT_MODIFIED: {
            "description": "Failed to modify the requested item as one was not found",
        },
    }
)
async def modify_item(request: ModifyItemRequest, id: int) -> ModifyItemResponse:
    patch_info = PatchItemInfo(request.name, request.price)

    patch_result = repository.patch_item_by_id(id, patch_info)

    if patch_result is None:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)

    return ModifyItemResponse(id, patch_result.name, patch_result.price)


@app.delete(
    path='/item/{id}',
    status_code=status.HTTP_200_OK,
)
async def delete_item(id: int) -> Response:
    repository.delete_item_by_id(id)

    return Response()


@app.post(
    path='/cart',
    status_code=status.HTTP_201_CREATED,
)
async def create_cart(response: Response):
    response.headers['location'] = path='/cart/1'
    return {'id': 1}
