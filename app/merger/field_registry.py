from app.merger.field_resolvers.string_resolver import StringResolver
from app.merger.field_resolvers.list_resolver import ListResolver
from app.merger.field_resolvers.object_list_resolver import ObjectListResolver
from app.merger.field_resolvers.dict_resolver import DictResolver
from app.merger.field_resolvers.numeric_resolver import NumericResolver
from app.merger.field_resolvers.skill_resolver import SkillResolver

from app.confidence.confidence_engine import ConfidenceEngine

from app.normalizers.email import EmailNormalizer
from app.normalizers.phone import PhoneNormalizer
from app.normalizers.skills import SkillNormalizer
from app.normalizers.location import LocationNormalizer
from app.normalizers.links import LinksNormalizer

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
        "resolver": DictResolver(),
        "normalizer": LocationNormalizer(),
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
        "resolver": SkillResolver(ConfidenceEngine()),
        "normalizer": None,
    },

    "links": {
        "resolver": DictResolver(),
        "normalizer": LinksNormalizer(),
    },

    "years_experience": {
        "resolver": NumericResolver(),
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