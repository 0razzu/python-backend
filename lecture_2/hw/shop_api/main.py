from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import Response

from lecture_2.hw.shop_api.dtos.requests import CreateItemRequest, ModifyItemRequest
from lecture_2.hw.shop_api.dtos.responses import ItemResponse, ModifyItemResponse, CreateCartResponse, GetCartResponse, \
    GetCartResponseItem, ErrorReason
from lecture_2.hw.shop_api.models import Item, PatchItemInfo, Cart
from lecture_2.hw.shop_api.store import repository
from lecture_2.hw.shop_api.store.errors import RepositoryException

app = FastAPI(title="Shop API")


@app.post(
    path='/item',
    status_code=status.HTTP_201_CREATED,
)
async def create_item(request: CreateItemRequest, response: Response) -> ItemResponse:
    item = Item(None, request.name, request.price, False)
    repository.insert_item(item)

    response.headers['location'] = f'/item/{item.id}'

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
    try:
        item = repository.get_item_by_id(id)
    except RepositoryException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=jsonable_encoder(ErrorReason('id')))

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

    try:
        repository.modify_item_by_id(id, item)
    except RepositoryException:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=jsonable_encoder(ErrorReason('id')))

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

    try:
        patch_result = repository.patch_item_by_id(id, patch_info)
    except RepositoryException:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail=jsonable_encoder(ErrorReason('id')))

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
async def create_cart(response: Response) -> CreateCartResponse:
    cart = Cart()

    repository.insert_cart(cart)

    response.headers['location'] = f'/cart/{cart.id}'

    return CreateCartResponse(cart.id)


@app.get(
    path='/cart/{id}',
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully returned the requested cart",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Failed to return the requested cart as one was not found",
        },
    },
)
async def get_cart_by_id(id: int) -> GetCartResponse:
    try:
        cart = repository.get_cart_by_id(id)
    except RepositoryException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=jsonable_encoder(ErrorReason('id')))

    return GetCartResponse(
        cart.id,
        [
            GetCartResponseItem(item.id, item.name, quan, not item.deleted)
            for item, quan in cart.items.items()
        ],
        sum(item.price * (0 if item.deleted else quan) for item, quan in cart.items.items()),
    )


@app.post(
    path='/cart/{cart_id}/add/{item_id}',
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully inserted",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Failed to insert as either the cart or the item was not found "
                           "(specified in the «details.field» field of the response body)",
        },
    },
)
async def add_item_to_cart(cart_id: int, item_id: int) -> Response:
    try:
        repository.add_item_to_cart(item_id, cart_id)
    except RepositoryException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=jsonable_encoder(ErrorReason(e.field)))

    return Response()
