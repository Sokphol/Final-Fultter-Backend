import re
import unicodedata


def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug."""
    text = str(text).lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def unique_slug(text: str, model, field: str = "slug", instance_id: int = None) -> str:
    """Generate a unique slug for a given model."""
    base_slug = slugify(text)
    slug = base_slug
    counter = 1
    while True:
        query = model.query.filter(getattr(model, field) == slug)
        if instance_id:
            query = query.filter(model.id != instance_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1
