import pytest
from app.models.document import Document


def test_document_creation(database):
    # GIVEN a Document instance
    document = Document(
        url="https://example.com/document.pdf", owner_id=1, owner_type="User"
    )
    database.session.add(document)
    database.session.commit()

    # THEN check the fields are defined correctly
    assert document.id is not None
    assert document.url == "https://example.com/document.pdf"
    assert document.owner_id == 1
    assert document.owner_type == "User"
    assert document.created_at is not None


def test_document_read_only_fields():
    # GIVEN a Document instance with an ID
    document = Document(
        url="https://example.com/document.pdf", owner_id=1, owner_type="User"
    )
    document.id = 1

    # THEN check that read-only fields cannot be modified
    with pytest.raises(AttributeError):
        document.url = "https://example.com/updated_document.pdf"
    with pytest.raises(AttributeError):
        document.owner_id = 2
    with pytest.raises(AttributeError):
        document.owner_type = "Product"


def test_document_representation():
    # GIVEN a Document instance
    document = Document(
        url="https://example.com/document.pdf", owner_id=1, owner_type="user"
    )

    # THEN check the representation of the document
    assert repr(document) == "<Document https://example.com/document.pdf>"


def test_document_string_conversion():
    # GIVEN a Document instance
    document = Document(
        url="https://example.com/document.pdf", owner_id=1, owner_type="User"
    )

    # THEN check the string conversion of the document
    assert str(document) == "https://example.com/document.pdf"

    # GIVEN a Document instance with an ID
    document = Document(
        url="https://example.com/document.pdf", owner_id=1, owner_type="User"
    )
    document.id = 1

    # THEN check that read-only fields cannot be modified
    with pytest.raises(AttributeError):
        document.url = "https://example.com/updated_document.pdf"

    with pytest.raises(AttributeError):
        document.owner_id = 2

    with pytest.raises(AttributeError):
        document.owner_type = "Product"
