from app.apis.secondary_views.about.models import AboutSchemaResponse
from app.apis.secondary_views.about.schema import schema_info


def test_schema_info():
    schema_info_data = schema_info()
    assert AboutSchemaResponse(**schema_info_data)
