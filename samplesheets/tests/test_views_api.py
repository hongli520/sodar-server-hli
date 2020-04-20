"""Tests for REST API views in the samplesheets app"""

import json
from unittest.case import skipIf

from django.urls import reverse

# Projectroles dependency
from projectroles.models import SODAR_CONSTANTS
from projectroles.plugins import get_backend_api
from projectroles.tests.test_models import RemoteSiteMixin, RemoteProjectMixin
from projectroles.tests.test_views_api import TestAPIViewsBase
from projectroles.tests.test_views_api_taskflow import TestTaskflowAPIBase

from samplesheets.io import SampleSheetIO
from samplesheets.models import Investigation, GenericMaterial, ISATab
from samplesheets.rendering import SampleSheetTableBuilder
from samplesheets.tests.test_io import SampleSheetIOMixin, SHEET_DIR
from samplesheets.tests.test_views_taskflow import SampleSheetTaskflowMixin
from samplesheets.tests.test_views import (
    TestViewsBase,
    IRODS_BACKEND_ENABLED,
    IRODS_BACKEND_SKIP_MSG,
    REMOTE_SITE_NAME,
    REMOTE_SITE_URL,
    REMOTE_SITE_DESC,
    REMOTE_SITE_SECRET,
)


# SODAR constants
PROJECT_TYPE_PROJECT = SODAR_CONSTANTS['PROJECT_TYPE_PROJECT']


# Local constants
SHEET_TSV_DIR = SHEET_DIR + 'i_small2/'
SHEET_PATH = SHEET_DIR + 'i_small2.zip'
SHEET_PATH_EDITED = SHEET_DIR + 'i_small2_edited.zip'
SHEET_PATH_ALT = SHEET_DIR + 'i_small2_alt.zip'


class TestSampleSheetAPIBase(SampleSheetIOMixin, TestAPIViewsBase):
    """Base view for samplesheets API views tests"""


# TODO: Move to test_views_api_taskflow
class TestSampleSheetAPITaskflowBase(
    SampleSheetIOMixin, SampleSheetTaskflowMixin, TestTaskflowAPIBase
):
    """Base samplesheets API view test class with Taskflow enabled"""

    def setUp(self):
        super().setUp()

        # Get iRODS backend for session access
        self.irods_backend = get_backend_api('omics_irods')
        self.assertIsNotNone(self.irods_backend)
        # self.irods_session = self.irods_backend.get_session()

        # Init project
        # Make project with owner in Taskflow and Django
        self.project, self.owner_as = self._make_project_taskflow(
            title='TestProject',
            type=PROJECT_TYPE_PROJECT,
            parent=self.category,
            owner=self.user,
            description='description',
        )

        # Import investigation
        self.investigation = self._import_isa_from_file(
            SHEET_PATH, self.project
        )
        self.study = self.investigation.studies.first()
        self.assay = self.study.assays.first()


class TestInvestigationRetrieveAPIView(TestSampleSheetAPIBase):
    """Tests for InvestigationRetrieveAPIView"""

    def setUp(self):
        super().setUp()

        # Import investigation
        self.investigation = self._import_isa_from_file(
            SHEET_PATH, self.project
        )
        self.study = self.investigation.studies.first()
        self.assay = self.study.assays.first()

    def test_get(self):
        """Test get() in InvestigationRetrieveAPIView"""
        url = reverse(
            'samplesheets:api_investigation_retrieve',
            kwargs={'project': self.project.sodar_uuid},
        )

        response = self.request_knox(url)

        self.assertEqual(response.status_code, 200)
        expected = {
            'sodar_uuid': str(self.investigation.sodar_uuid),
            'identifier': self.investigation.identifier,
            'file_name': self.investigation.file_name,
            'project': str(self.project.sodar_uuid),
            'title': self.investigation.title,
            'description': self.investigation.description,
            'irods_status': False,
            'parser_version': self.investigation.parser_version,
            'archive_name': self.investigation.archive_name,
            'comments': self.investigation.comments,
            'studies': {
                str(self.study.sodar_uuid): {
                    'identifier': self.study.identifier,
                    'file_name': self.study.file_name,
                    'title': self.study.title,
                    'description': self.study.description,
                    'comments': self.study.comments,
                    'assays': {
                        str(self.assay.sodar_uuid): {
                            'file_name': self.assay.file_name,
                            'technology_platform': self.assay.technology_platform,
                            'technology_type': self.assay.technology_type,
                            'measurement_type': self.assay.measurement_type,
                            'comments': self.assay.comments,
                        }
                    },
                }
            },
        }
        self.assertEqual(json.loads(response.content), expected)


class TestSampleSheetImportAPIView(TestSampleSheetAPIBase):
    """Tests for SampleSheetImportAPIView"""

    def test_post_zip(self):
        """Test SampleSheetImportAPIView post() with a zip archive"""

        # Assert preconditions
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 0
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 0)

        url = reverse(
            'samplesheets:api_import',
            kwargs={'project': self.project.sodar_uuid},
        )

        with open(SHEET_PATH, 'rb') as file:
            post_data = {'file': file}
            response = self.request_knox(
                url, method='POST', format='multipart', data=post_data
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 1)

    def test_post_tsv(self):
        """Test SampleSheetImportAPIView post() with ISAtab tsv files"""

        # Assert preconditions
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 0
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 0)

        url = reverse(
            'samplesheets:api_import',
            kwargs={'project': self.project.sodar_uuid},
        )
        tsv_file_i = open(SHEET_TSV_DIR + 'i_small2.txt', 'r')
        tsv_file_s = open(SHEET_TSV_DIR + 's_small2.txt', 'r')
        tsv_file_a = open(SHEET_TSV_DIR + 'a_small2.txt', 'r')
        post_data = {
            'file_investigation': tsv_file_i,
            'file_study': tsv_file_s,
            'file_assay': tsv_file_a,
        }

        response = self.request_knox(
            url, method='POST', format='multipart', data=post_data
        )

        tsv_file_i.close()
        tsv_file_s.close()
        tsv_file_a.close()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 1)

    def test_post_replace(self):
        """Test replacing sheets"""

        self.investigation = self._import_isa_from_file(
            SHEET_PATH, self.project
        )

        # Assert preconditions
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 1)
        self.assertIsNone(GenericMaterial.objects.filter(name='0816').first())

        url = reverse(
            'samplesheets:api_import',
            kwargs={'project': self.project.sodar_uuid},
        )

        with open(SHEET_PATH_EDITED, 'rb') as file:
            post_data = {'file': file}
            response = self.request_knox(
                url, method='POST', format='multipart', data=post_data
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 2)
        # Added material
        self.assertIsNotNone(
            GenericMaterial.objects.filter(name='0816').first()
        )

    def test_post_replace_alt_sheet(self):
        """Test replacing with an alternative sheet and irods_status=False"""

        self.investigation = self._import_isa_from_file(
            SHEET_PATH, self.project
        )

        # Assert preconditions
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 1)

        url = reverse(
            'samplesheets:api_import',
            kwargs={'project': self.project.sodar_uuid},
        )
        with open(SHEET_PATH_ALT, 'rb') as file:
            post_data = {'file': file}
            response = self.request_knox(
                url, method='POST', format='multipart', data=post_data
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 2)

    def test_post_replace_alt_sheet_irods(self):
        """Test replacing with an alternative sheet and irods_status=True (should fail)"""

        self.investigation = self._import_isa_from_file(
            SHEET_PATH, self.project
        )
        self.investigation.irods_status = True  # fake irods status
        self.investigation.save()

        # Assert preconditions
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 1)

        url = reverse(
            'samplesheets:api_import',
            kwargs={'project': self.project.sodar_uuid},
        )
        with open(SHEET_PATH_ALT, 'rb') as file:
            post_data = {'file': file}
            response = self.request_knox(
                url, method='POST', format='multipart', data=post_data
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            Investigation.objects.filter(project=self.project).count(), 1
        )
        self.assertEqual(ISATab.objects.filter(project=self.project).count(), 1)


# TODO: Move to test_views_api_taskflow
@skipIf(not IRODS_BACKEND_ENABLED, IRODS_BACKEND_SKIP_MSG)
class TestIrodsCollsCreateAPIView(TestSampleSheetAPITaskflowBase):
    """Tests for IrodsCollsCreateAPIView"""

    def test_post(self):
        """Test post() in IrodsCollsCreateAPIView"""

        # Assert preconditions
        self.assertEqual(self.investigation.irods_status, False)

        url = reverse(
            'samplesheets:api_irods_colls_create',
            kwargs={'project': self.project.sodar_uuid},
        )

        response = self.request_knox(url, method='POST', data=self.request_data)

        self.assertEqual(response.status_code, 200)
        self.investigation.refresh_from_db()
        self.assertEqual(self.investigation.irods_status, True)

    def test_post_created(self):
        """Test post() with already created collections (should fail)"""

        # Set up iRODS collections
        self._make_irods_colls(self.investigation)

        # Assert preconditions
        self.assertEqual(self.investigation.irods_status, True)

        url = reverse(
            'samplesheets:api_irods_colls_create',
            kwargs={'project': self.project.sodar_uuid},
        )

        response = self.request_knox(url, method='POST', data=self.request_data)

        self.assertEqual(response.status_code, 400)


# NOTE: Not yet standardized api, use old base class to test
class TestRemoteSheetGetAPIView(
    RemoteSiteMixin, RemoteProjectMixin, TestViewsBase
):
    """Tests for RemoteSheetGetAPIView"""

    def setUp(self):
        super().setUp()

        # Create target site
        self.target_site = self._make_site(
            name=REMOTE_SITE_NAME,
            url=REMOTE_SITE_URL,
            mode=SODAR_CONSTANTS['SITE_MODE_TARGET'],
            description=REMOTE_SITE_DESC,
            secret=REMOTE_SITE_SECRET,
        )

        # Create target project
        self.target_project = self._make_remote_project(
            project_uuid=self.project.sodar_uuid,
            site=self.target_site,
            level=SODAR_CONSTANTS['REMOTE_LEVEL_READ_ROLES'],
        )

        # Import investigation
        self.investigation = self._import_isa_from_file(
            SHEET_PATH, self.project
        )
        self.study = self.investigation.studies.first()

    def test_get_tables(self):
        """Test getting the investigation as rendered tables"""
        response = self.client.get(
            reverse(
                'samplesheets:api_remote_get',
                kwargs={
                    'project': self.project.sodar_uuid,
                    'secret': REMOTE_SITE_SECRET,
                },
            )
        )

        tb = SampleSheetTableBuilder()
        expected = {
            'studies': {
                str(self.study.sodar_uuid): tb.build_study_tables(self.study)
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    def test_get_isatab(self):
        """Test getting the investigation as ISAtab"""
        response = self.client.get(
            reverse(
                'samplesheets:api_remote_get',
                kwargs={
                    'project': self.project.sodar_uuid,
                    'secret': REMOTE_SITE_SECRET,
                },
            ),
            {'isa': '1'},
        )

        sheet_io = SampleSheetIO()
        expected = sheet_io.export_isa(self.investigation)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)