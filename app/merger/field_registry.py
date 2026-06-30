from app.merger.field_resolvers.string_resolver import StringResolver
from app.merger.field_resolvers.list_resolver import ListResolver
from app.merger.field_resolvers.object_list_resolver import ObjectListResolver

from app.normalizers.email import EmailNormalizer
from app.normalizers.phone import PhoneNormalizer
from app.normalizers.skills import SkillNormalizer

FIELD_CONFIG = {

    "full_name": {
        "resolver": StringResolver(),
        "normalizer": None,
    },

    "headline": {
        "resolver": StringResolver(),
        "normalizer": None,
    },

    "location": {
        "resolver": StringResolver(),
        "normalizer": None,
    },

    "emails": {
        "resolver": ListResolver(),
        "normalizer": EmailNormalizer(),
    },

    "phones": {
        "resolver": ListResolver(),
        "normalizer": PhoneNormalizer(),
    },

    "skills": {
        "resolver": ListResolver(),
        "normalizer": SkillNormalizer(),
    },

    "links": {
        "resolver": ListResolver(),
        "normalizer": None,
    },

    "experience": {
        "resolver": ObjectListResolver(),
        "normalizer": None,
    },

    "education": {
        "resolver": ObjectListResolver(),
        "normalizer": None,
    }

}