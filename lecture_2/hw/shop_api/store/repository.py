from lecture_2.hw.shop_api.models import Item, PatchItemInfo
from lecture_2.hw.shop_api.store.data import id_generator, items, DBItem


def insert_item(item: Item) -> int:
    id = next(id_generator)

    item.deleted = False
    item.id = id

    items[id] = DBItem(item.name, item.price, item.deleted)

    return id


def _get_item_by_id(id: int) -> DBItem | None:
    db_item = items.get(id)

    if db_item is None or db_item.deleted:
        return None

    return db_item


def get_item_by_id(id: int) -> Item | None:
    db_item = _get_item_by_id(id)

    if db_item is None:
        return None

    return Item(id, db_item.name, db_item.price, db_item.deleted)


def check_item_by_id(id: int) -> bool:
    return items.get(id) is not None


def modify_item_by_id(id: int, item: Item) -> bool:
    db_item = _get_item_by_id(id)

    if db_item is None:
        return False

    item.deleted = False
    item.id = id

    items[id] = DBItem(item.name, item.price, item.deleted)

    return True


def patch_item_by_id(id: int, patch_info: PatchItemInfo) -> PatchItemInfo | None:
    db_item = _get_item_by_id(id)

    if db_item is None:
        return None

    patch_result = PatchItemInfo()
    if patch_info.name != db_item.name:
        patch_result.name = patch_info.name
    if patch_info.price != db_item.price:
        patch_result.price = patch_info.price

    items[id].name = patch_info.name
    items[id].price = patch_info.price

    return patch_result


def delete_item_by_id(id: int) -> bool:
    db_item = _get_item_by_id(id)

    if db_item is None:
        return False

    items[id].deleted = True

    return True
