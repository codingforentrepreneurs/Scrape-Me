"""
This is an example single-page Django application
that serves HTML templates from a directory.

To learn more about building single-page Django applications,
watch https://www.youtube.com/watch?v=F91BTQnxV6w

Waitress is used over Gunicorn to allow
Windows users to run the application easily.
"""
import logging
import os
import pathlib
import random
import sys

import hupper
from django.conf import settings
from django.core.management.utils import get_random_secret_key
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render
from django.urls import path
from django.utils import timezone
from faker import Faker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

SECRET_KEY = get_random_secret_key()
BASE_DIR = pathlib.Path(__file__).resolve().parent
DJANGO_TEMPLATES = BASE_DIR / "django_templates"
HTML_TEMPLATES = BASE_DIR / "html_templates"
STATICFILES_DIRS = [HTML_TEMPLATES]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

settings.configure(
    DEBUG=True,
    SECRET_KEY=f"{SECRET_KEY}",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ],
    STATICFILES_DIRS=STATICFILES_DIRS,
    STATICFILES_STORAGE=STATICFILES_STORAGE,
    STATIC_URL="/static/",
    APPEND_SLASH=True,
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [DJANGO_TEMPLATES, str(HTML_TEMPLATES)],
        }
    ],
)


def generate_blog_post(fake):
    return {
        "title": fake.sentence(nb_words=6),
        "author": fake.name(),
        "slug": fake.slug(),
        "pub_date": fake.date(),
        "content": "\n\n".join(fake.paragraphs(nb=random.randint(3, 10))),
    }


def fake_blog_post_list_view(request):
    fake = Faker()
    max_entries = request.GET.get("max-entries", 10)
    blog_posts = [generate_blog_post(fake) for _ in range(int(max_entries))]
    context = {
        "object_list": blog_posts,
    }
    return render(request, "fake/blog/list.html", context)


def fake_blog_post_detail_view(request, slug=None):
    fake = Faker()
    instance = generate_blog_post(fake)
    context = {
        "instance": instance,
        "slug": slug,
    }
    return render(request, "fake/blog/detail.html", context)


def fake_table_view(request):
    table_data = []
    header = ["id", "name", "email", "phone", "address"]
    max_entries = request.GET.get("max-entries", 50)
    for i, _ in enumerate(range(int(max_entries))):
        fake = Faker()
        table_data.append(
            {
                "id": i + 1 * random.randint(1, 10_000),
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "address": fake.address(),
            }
        )
    context = {"table_data": table_data, "header": header}
    return render(request, "fake/table.html", context)


template_mapping = {}

default_context = {
    "title": "Django HTML Templates",
    "description": "A collection of HTML templates for Django",
    "timestamp": timezone.now(),
}


def render_template(request, *args, **kwargs):
    path_as_key = request.path
    if path_as_key.startswith("/"):
        path_as_key = path_as_key[1:]
    template_name = template_mapping.get(path_as_key)
    return render(request, template_name, default_context)


routes = [
    path("fake/table/", fake_table_view),
    path("fake/blog/", fake_blog_post_list_view),
    path("fake/blog/<slug:slug>/", fake_blog_post_detail_view),
]
for doc in HTML_TEMPLATES.glob("**/*.html"):
    # print(doc)
    name = f"{doc.name}_view"
    abs_doc_path = pathlib.Path(doc).resolve()
    abs_html_templates_path = HTML_TEMPLATES.resolve()
    template_path = abs_doc_path.relative_to(abs_html_templates_path)
    url_path = f"{template_path}".replace(".html", "").strip()
    if url_path.endswith("index"):
        url_path = url_path.replace("index", "")
    if not url_path.endswith("/"):
        url_path = f"{url_path}/"
    if url_path == "/":
        url_path = ""
    template_mapping[url_path] = template_path
    django_url_path = path(
        url_path,
        render_template,
    )
    routes.append(django_url_path)


urlpatterns = routes

application = get_wsgi_application()


def start_server():
    try:
        from waitress import serve
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Waitress. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    port = os.environ.get("PORT")
    if port is None:
        if len(sys.argv) > 1:
            port = sys.argv[1]
        else:
            port = "8101"

    if not port.isdigit():
        raise ValueError("Port must be a number")

    logger.info(f"Starting development server at http://localhost:{port}/")
    logger.info("Using hupper to watch for file changes. Hit CTRL-C to stop.")
    serve(application, port=port)


if __name__ == "__main__":
    reloader = hupper.start_reloader("app.start_server")
    start_server()
