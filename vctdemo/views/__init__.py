#

# enable fa.jquery
from formalchemy.ext.zope import FieldSet
from fa.jquery import renderers as jquery
FieldSet.default_renderers.update(jquery.default_renderers)

