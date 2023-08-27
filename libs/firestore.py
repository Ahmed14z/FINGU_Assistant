import libs.firestore_async as db
from firebase_admin import firestore

async def addDoc(collection, data):
    """
    Adds a document to a collection in the database.

    :param collection: The name of the collection to add the document to (string).
    :param document: The ID of the document to add (string).
    :param data: The data to be added to the document (dict).
    :param db: The database object to use (optional, default=db).

    :return: The output of the set operation (dict).
    """
    newDoc = {"createdAt": firestore.SERVER_TIMESTAMP, "data": data}
    doc_ref = db.db.collection(str(collection)).document()
    output = await doc_ref.set(newDoc)
    return output


async def readCol(collection, filterArg):
    """
    Read documents from a collection based on a filter.

    Args:
        collection (str): The name of the collection to read from.
        filter (dict): A dictionary representing the filter to apply to the documents. example of filter is ("capital", "==", True)

    Returns:
        An asynchronous iterator over the documents in the collection that match the filter.
    """
    docs = (
        db.db.collection(collection)
        .limit(100)
        .order_by("createdAt", direction=firestore.Query.DESCENDING)
        .stream()
    )
    result = []
    for doc in docs:
        data = doc.to_dict().get('data')
        result.append(data)
    return result
