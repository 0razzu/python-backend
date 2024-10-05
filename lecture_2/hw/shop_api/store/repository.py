from lecture_2.hw.shop_api.models import Item, PatchItemInfo, Cart
from lecture_2.hw.shop_api.store.data import generate_id, items, DBItem, carts, DBCart
from lecture_2.hw.shop_api.store.errors import RepositoryException, RepositoryErrorCode
from lecture_2.hw.shop_api.views import CartView


def insert_item(item: Item) -> int:
    id = generate_id()

    item.deleted = False
    item.id = id

    items[id] = DBItem(item.name, item.price, item.deleted)

    return id


def _get_item_by_id(id: int) -> DBItem:
    db_item = items.get(id)

    if db_item is None or db_item.deleted:
        raise RepositoryException(RepositoryErrorCode.NOT_FOUND, 'id')

    return db_item


def get_item_by_id(id: int) -> Item:
    db_item = _get_item_by_id(id)

    return Item(id, db_item.name, db_item.price, db_item.deleted)


def get_item_by_id_with_deleted(id: int) -> Item:
    db_item = items[id]

    return Item(id, db_item.name, db_item.price, db_item.deleted)


def check_item_by_id(id: int) -> bool:
    db_item = items.get(id)

    return db_item is not None and not db_item.deleted


def get_items(
        offset: int = 0,
        limit: int = 5000,
        min_price: float | None = None,
        max_price: float | None = None,
        show_deleted: bool = False,
) -> list[Item]:
    db_items = sorted(items.items(), key=lambda entry: entry[0])
    if min_price is not None:
        db_items = filter(lambda entry: entry[1].price >= min_price, db_items)
    if max_price is not None:
        db_items = filter(lambda entry: entry[1].price <= max_price, db_items)
    if not show_deleted:
        db_items = filter(lambda entry: not entry[1].deleted, db_items)
    db_items = list(db_items)[offset: offset + limit]

    return [Item(id, db_item.name, db_item.price, db_item.deleted) for id, db_item in db_items]


def modify_item_by_id(id: int, item: Item) -> None:
    db_item = _get_item_by_id(id)

    item.deleted = False
    item.id = id

    items[id] = DBItem(item.name, item.price, item.deleted)


def patch_item_by_id(id: int, patch_info: PatchItemInfo) -> PatchItemInfo:
    db_item = _get_item_by_id(id)

    patch_result = PatchItemInfo()
    if patch_info.name != db_item.name:
        patch_result.name = patch_info.name
    if patch_info.price != db_item.price:
        patch_result.price = patch_info.price

    items[id].name = patch_info.name
    items[id].price = patch_info.price

    return patch_result


def delete_item_by_id(id: int) -> bool:
    try:
        db_item = _get_item_by_id(id)
        items[id].deleted = True
    except RepositoryException:
        return False

    return True


def insert_cart(cart: Cart) -> int:
    id = generate_id()

    cart.id = id
    carts[id] = DBCart()

    return id


def get_cart_by_id(id: int) -> Cart:
    db_cart = carts.get(id)

    if db_cart is None:
        raise RepositoryException(RepositoryErrorCode.NOT_FOUND, 'id')

    cart = Cart(id)
    cart.items = {
        get_item_by_id_with_deleted(item_id): item_quan
        for item_id, item_quan in db_cart.items.items()
    }

    return cart


def get_cart_views(
        offset: int = 0,
        limit: int = 5000,
        min_price: float | None = None,
        max_price: float | None = None,
        min_quantity: int | None = None,
        max_quantity: int | None = None,
) -> list[CartView]:
    db_cart_views = []
    for cart_id, db_cart in sorted(carts.items(), key=lambda entry: entry[0]):
        db_cart_view_items = [
            {'id': item_id, 'item': items[item_id], 'quan': quan}
            for item_id, quan in db_cart.items.items()
        ]

        price = 0
        quan = 0
        for item_view in db_cart_view_items:
            item_price = item_view['item'].price
            item_quan = 0 if item_view['item'].deleted else item_view['quan']

            price += item_price * item_quan
            quan += item_quan

        db_cart_views.append({
            'id': cart_id,
            'items': db_cart_view_items,
            'price': price,
            'quan': quan,
        })

    if min_price is not None:
        db_cart_views = filter(lambda cart: cart['price'] >= min_price, db_cart_views)
    if max_price is not None:
        db_cart_views = filter(lambda cart: cart['price'] <= max_price, db_cart_views)
    if min_quantity is not None:
        db_cart_views = filter(lambda cart: cart['quan'] >= min_quantity, db_cart_views)
    if max_quantity is not None:
        db_cart_views = filter(lambda cart: cart['quan'] <= max_quantity, db_cart_views)
    db_cart_views = list(db_cart_views)[offset: offset + limit]

    return [CartView(
        cart['id'],
        {Item(
            item['id'],
            item['item'].name,
            item['item'].price,
            item['item'].deleted
        ): item['quan'] for item in cart['items']},
        cart['price'],
        cart['quan'],
    ) for cart in db_cart_views]


def add_item_to_cart(item_id: int, cart_id: int):
    db_cart = carts.get(cart_id)

    if db_cart is None:
        raise RepositoryException(RepositoryErrorCode.NOT_FOUND, 'cart_id')

    if not check_item_by_id(item_id):
        raise RepositoryException(RepositoryErrorCode.NOT_FOUND, 'item_id')

    db_cart.items[item_id] = db_cart.items.get(item_id, 0) + 1
