from django.urls import reverse_lazy

# Swagger Setting
# https://drf-yasg.readthedocs.io/en/stable/settings.html

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "LOGIN_URL": reverse_lazy("admin:login"),
    "LOGOUT_URL": reverse_lazy("admin:logout"),
    "VALIDATOR_URL": None,
    "REFETCH_SCHEMA_WITH_AUTH": True,
    "REFETCH_SCHEMA_ON_LOGOUT": True,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Authorize with token, Format: Bearer <token> or token <token>",
        },
    },
}
