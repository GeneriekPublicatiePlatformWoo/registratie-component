from django.contrib.contenttypes.models import ContentType
from django.test import override_settings
from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.utils.translation import gettext as _

from django_webtest import DjangoWebtestResponse, WebTest
from furl import furl
from maykin_2fa.test import disable_admin_mfa
from timeline_logger.models import TimelineLog

from woo_publications.accounts.tests.factories import UserFactory
from woo_publications.publications.tests.factories import PublicationFactory

from ..constants import Events
from ..models import TimelineLogProxy


# must decorate the class, since at the test-level the wsgi app is already being
# initialized and overriding the setting is too late
@override_settings(SESSION_ENGINE="django.contrib.sessions.backends.db")
@disable_admin_mfa()
class AuditLogAdminTests(WebTest):

    list_url = reverse_lazy("admin:logging_timelinelogproxy_changelist")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.superuser = UserFactory.create(superuser=True)

    def assertNumLogsDisplayed(self, response, amount: int):
        result_rows = response.pyquery("#result_list tbody tr")
        self.assertEqual(len(result_rows), amount)

    def test_auth_required(self):
        response = self.app.get(self.list_url, status=302)

        expected_next = furl(reverse("admin:login")).add({"next": str(self.list_url)})
        self.assertRedirects(response, str(expected_next))

    def test_nobody_has_write_permissions(self):
        """
        Test that not even the superusers have write permissions.
        """
        self.client.force_login(user=self.superuser)

        with (
            self.subTest("original admin integration disabled"),
            self.assertRaises(NoReverseMatch),
        ):
            reverse("admin:timeline_logger_timelinelog_changelist")

        record = TimelineLogProxy.objects.create(
            extra_data={
                "event": Events.create,
                "acting_user": {"identifier": "admin", "display_name": "Superadmin"},
            }
        )

        with self.subTest("change blocked"):
            change_page_url = reverse(
                "admin:logging_timelinelogproxy_change",
                args=(record.pk,),
            )

            response = self.client.post(change_page_url)

            self.assertEqual(response.status_code, 403)

        with self.subTest("add blocked"):
            add_page_url = reverse("admin:logging_timelinelogproxy_add")

            response = self.client.post(add_page_url)

            self.assertEqual(response.status_code, 403)

        with self.subTest("delete blocked"):
            delete_page_url = reverse(
                "admin:logging_timelinelogproxy_delete",
                args=(record.pk,),
            )

            response = self.client.post(delete_page_url)

            self.assertEqual(response.status_code, 403)

    def test_displays_valid_and_broken_logrecords_without_crashing(self):
        # it's possible log records get created that don't fit out constraints - these
        # may not cause the admin list or detail view to crash
        TimelineLog.objects.create(extra_data=None)
        TimelineLog.objects.create(extra_data={})
        TimelineLog.objects.create(extra_data=[])
        TimelineLog.objects.create(
            extra_data={
                "event": 42.0,
                "acting_user": ["wrong", "type"],
            }
        )

        response = self.app.get(self.list_url, user=self.superuser)

        self.assertEqual(response.status_code, 200)
        self.assertNumLogsDisplayed(response, 4)

    def test_event_human_readable_display(self):
        # a broken record
        TimelineLog.objects.create(extra_data=None)
        # a valid record
        TimelineLogProxy.objects.create(
            extra_data={
                "event": Events.create,
                "acting_user": {"identifier": "admin", "display_name": "Superadmin"},
            }
        )

        response = self.app.get(self.list_url, user=self.superuser)

        self.assertContains(response, _("Record created"))
        self.assertContains(response, "unknown")

    def test_acting_user_displayed(self):
        # a broken record
        TimelineLog.objects.create(extra_data=None)
        # a valid record
        TimelineLogProxy.objects.create(
            extra_data={
                "event": Events.create,
                "acting_user": {"identifier": "admin", "display_name": "Superadmin"},
            }
        )
        # a valid record with related django user
        django_user = UserFactory.create()
        TimelineLogProxy.objects.create(
            user=django_user,
            extra_data={
                "event": Events.create,
                "acting_user": {"identifier": "1234", "display_name": "Django User"},
            },
        )

        response = self.app.get(self.list_url, user=self.superuser)

        self.assertEqual(response.status_code, 200)
        self.assertNumLogsDisplayed(response, 3)

        self.assertContains(
            response,
            _("{name} ({identifier})").format(name="Superadmin", identifier="admin"),
        )
        self.assertContains(
            response,
            _("{name} ({identifier}, local user ID: {django_id})").format(
                name="Django User",
                identifier="1234",
                django_id=django_user.id,
            ),
        )

    def test_link_to_related_object(self):
        with self.subTest("related object enabled in admin"):
            publication = PublicationFactory.create(
                officiele_titel="Publicatie voor logging test"
            )
            publication_change_link = reverse(
                "admin:publications_publication_change", args=(publication.pk,)
            )
            TimelineLogProxy.objects.create(
                content_object=publication,
                extra_data={
                    "event": Events.create,
                    "acting_user": {
                        "identifier": "testsuite",
                        "display_name": "Automated tests",
                    },
                },
            )
            response: DjangoWebtestResponse = self.app.get(
                self.list_url, user=self.superuser
            )

            publication_admin_view = response.click(
                description="Publicatie voor logging test",
                href=publication_change_link,
            )

            self.assertEqual(
                publication_admin_view.request.path, publication_change_link
            )

        with self.subTest("related object not enabled in admin"):
            # Use a content type since those are not exposed in the admin by Django.
            log_content_type = ContentType.objects.get_for_model(TimelineLog)
            TimelineLogProxy.objects.create(
                content_object=log_content_type,
                extra_data={
                    "event": Events.read,
                    "acting_user": {
                        "identifier": "testsuite",
                        "display_name": "Automated tests",
                    },
                },
            )

            response = self.app.get(self.list_url, user=self.superuser)

            self.assertEqual(response.status_code, 200)

    def test_search_behaviour(self):
        # test the expected behaviour when entering search terms in the search bar
        self.app.set_user(self.superuser)
        TimelineLogProxy.objects.create(
            extra_data={
                "event": Events.read,
                "acting_user": {"identifier": "1234", "display_name": "Some user"},
            },
        )
        TimelineLogProxy.objects.create(
            extra_data={
                "event": Events.read,
                "acting_user": {
                    "identifier": "testsuite",
                    "display_name": "Automated tests",
                },
                "_cached_object_repr": "foobar",
            },
        )
        # broken audit log entry
        TimelineLogProxy.objects.create(
            extra_data={
                "event": Events.read,
                "acting_user": {
                    "identifier": None,
                    "display_name": None,
                },
                "_cached_object_repr": None,
            },
        )

        with self.subTest("search on user identifier"):
            response = self.app.get(self.list_url, {"q": "1234"})

            self.assertEqual(response.status_code, 200)
            self.assertNumLogsDisplayed(response, 1)
            self.assertContains(response, "1234")
            self.assertNotContains(response, "testsuite")

        with self.subTest("search on user identifier"):
            response = self.app.get(self.list_url, {"q": "Automated"})

            self.assertEqual(response.status_code, 200)
            self.assertNumLogsDisplayed(response, 1)
            self.assertNotContains(response, "1234")
            self.assertContains(response, "testsuite")

        with self.subTest("search on cached_object_repr"):
            response = self.app.get(self.list_url, {"q": "foobar"})

            self.assertEqual(response.status_code, 200)
            self.assertNumLogsDisplayed(response, 1)
            self.assertContains(response, "foobar")

    def test_no_excessive_queries_for_content_object(self):
        # create a 100 records to fill the admin - can't use bulk create because that
        # skips the save method :)
        log_content_type = ContentType.objects.get_for_model(TimelineLog)
        for __ in range(100):
            TimelineLogProxy.objects.create(
                object_id=log_content_type.pk,
                content_type=ContentType.objects.get_for_model(ContentType),
                extra_data={
                    "event": Events.read,
                    "acting_user": {
                        "identifier": "testsuite",
                        "display_name": "Automated tests",
                    },
                },
            )
        # do login to trigger auth related queries early
        self.app.get(reverse("admin:index"), user=self.superuser)

        # Expected queries:
        #
        #  1. mozilla-django-oidc-db config grabbing (not sure why?)
        #  2. select django session for authenticated user
        #  3. look up the super user from the session's user_id
        #  4. get total count of log records
        #  5. get total count of log records (bis)
        #  6. select the log records to display
        #  7. get the admin index configuration
        #  8. get the admin index configuration (second aspect)
        #  9. get the admin index configuration (third aspect)
        # 10. get the timestamp min/max for the date_hierarchy links
        # 11. another query related to date_hierarchy I think
        with self.assertNumQueries(11):
            response = self.app.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertNumLogsDisplayed(response, 100)

    def test_event_search(self):
        self.app.set_user(self.superuser)
        publication = PublicationFactory.create(
            officiele_titel="Publicatie voor logging test"
        )
        TimelineLogProxy.objects.create(
            content_object=publication,
            extra_data={
                "event": Events.create,
                "acting_user": {
                    "identifier": "1",
                    "display_name": "User One",
                },
            },
        )
        TimelineLogProxy.objects.create(
            content_object=publication,
            extra_data={
                "event": Events.update,
                "acting_user": {
                    "identifier": "2",
                    "display_name": "User Two",
                },
            },
        )
        change_list_page = self.app.get(self.list_url)

        with self.subTest("filter on create event"):
            # simulate clicking the filter on events
            filtered_response = change_list_page.click(description=_("Record created"))

            self.assertEqual(filtered_response.status_code, 200)
            self.assertNumLogsDisplayed(filtered_response, 1)
            self.assertContains(filtered_response, "User One")

        with self.subTest("filter on update event"):
            # simulate clicking the filter on events
            filtered_response = change_list_page.click(description=_("Record updated"))

            self.assertEqual(filtered_response.status_code, 200)
            self.assertNumLogsDisplayed(filtered_response, 1)
            self.assertContains(filtered_response, "User Two")
