.. _developers_audit_logging:

Audit logging
=============

WOO Publications ships some high and low level Python API's to ensure user actions
are properly logged in the audit log.

You can find these in the top-level module :mod:`woo_publications.logging.service`.

Admin integration
-----------------

Mixins/helper classes for :class:`django.contrib.admin.ModelAdmin` and related classes.

.. autoclass:: woo_publications.logging.service.AdminAuditLogMixin
    :members:

.. autoclass:: woo_publications.logging.service.AuditLogInlineformset
    :members:

.. autofunction:: woo_publications.logging.service.get_logs_link

DRF integration
---------------

Mixins are available to drop into a :class:`rest_framework.views.APIView` or
:class:`rest_framework.viewsets.ViewSet` class.

.. autoclass:: woo_publications.logging.service.AuditTrailViewSetMixin
    :members:

**Individual mixins**

.. autoclass:: woo_publications.logging.service.AuditTrailCreateMixin
    :members:

.. autoclass:: woo_publications.logging.service.AuditTrailRetrieveMixin
    :members:

.. autoclass:: woo_publications.logging.service.AuditTrailUpdateMixin
    :members:

.. autoclass:: woo_publications.logging.service.AuditTrailDestroyMixin
    :members:

Low level API
-------------

The low-level API is used by the high-level API above. It may be required in certain
specialized cases.

.. autofunction:: woo_publications.logging.service.audit_api_create

.. autofunction:: woo_publications.logging.service.audit_api_read

.. autofunction:: woo_publications.logging.service.audit_api_update

.. autofunction:: woo_publications.logging.service.audit_api_delete

.. autofunction:: woo_publications.logging.service.audit_admin_create

.. autofunction:: woo_publications.logging.service.audit_admin_read

.. autofunction:: woo_publications.logging.service.audit_admin_update

.. autofunction:: woo_publications.logging.service.audit_admin_delete
