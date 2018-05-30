"""Tests for models in the samplesheets app"""

# NOTE: Retraction and sharing data not yet tested, to be implemented
# TODO: Test validation rules and uniqueness constraints

from test_plus.test import TestCase

from django.forms.models import model_to_dict
from django.utils import timezone

# Projectroles dependency
from projectroles.models import Role, OMICS_CONSTANTS
from projectroles.tests.test_models import ProjectMixin, RoleAssignmentMixin

from ..models import Investigation, Study, Assay, Protocol, Process, \
    GenericMaterial, NOT_AVAILABLE_STR


# Local constants --------------------------------------------------------------


INV_IDENTIFIER = 'Investigation identifier'
INV_FILE_NAME = 'i_Investigation.txt'
INV_TITLE = 'Investigation'

STUDY_IDENTIFIER = 'Study identifier'
STUDY_FILE_NAME = 's_study.txt'
STUDY_TITLE = 'study'

PROTOCOL_NAME = 'sample collection'
PROTOCOL_TYPE = 'sample collection'
PROTOCOL_PARAMS = [
    'library kit', 'library selection', 'mid', 'library source',
    'library layout', 'library strategy']
PROTOCOL_URI = 'pmid:11314272'
PROTOCOL_VERSION = '1'
PROTOCOL_COMPONENTS = '454 GS FLX Titanium'

ASSAY_IDENTIFIER = 'Study identifier'
ASSAY_FILE_NAME = 'a_assay.txt'
ASSAY_MEASURE_TYPE = 'environmental gene survey'
ASSAY_TECH_PLATFORM = '454 GS FLX'
ASSAY_TECH_TYPE = 'nucleotide sequencing'

SOURCE_NAME = 'patient0'
SOURCE_UNIQUE_NAME = 'p1-s1-a1-patient0-1-1'
SOURCE_CHARACTERISTICS = {
    'Age': {
        'unit': {
            'name': 'day',
            'accession': 'http://purl.obolibrary.org/obo/UO_0000033',
            'ontology_name': 'UO'
        },
        'value': '2423'
    }
}

SAMPLE_NAME = 'patient0-s1'
SAMPLE_UNIQUE_NAME = 'p1-s1-a1-patient0-s1'
SAMPLE_CHARACTERISTICS = {'Tissue': {'unit': None, 'value': 'N'}}

MATERIAL_NAME = 'extract'
MATERIAL_UNIQUE_NAME = 'p1-s1-a1-extract-1-1'
MATERIAL_TYPE = 'Extract Name'

DATA_NAME = 'file.gz'
DATA_UNIQUE_NAME = 'p1-s1-a1-file.gz-COL1'
DATA_TYPE = 'Raw Data File'

PROCESS_NAME = 'Process'
PROCESS_UNIQUE_NAME = 'p1-s1-a1-process-1-1'
PROCESS_PARAM_VALUES = {'INSERT_SIZE': {'unit': None, 'value': '481'}}
PROCESS_PERFORMER = 'Alice Example'
PROCESS_PERFORM_DATE = timezone.now()

DEFAULT_DESCRIPTION = 'Description'
DEFAULT_COMMENTS = {'comment': 'value'}


# Helper mixins ----------------------------------------------------------------


class SampleSheetModelMixin:
    """Helpers for samplesheets models creation"""

    @classmethod
    def _make_investigation(
            cls, identifier, file_name, project, title, description,
            retraction_data=None, sharing_data=None, comments=None):
        """Create Investigation in database"""
        values = {
            'identifier': identifier,
            'file_name': file_name,
            'project': project,
            'title': title,
            'description': description,
            'comments': comments,
            'active': True}     # NOTE: Must explicitly set active to True
        obj = Investigation(**values)
        obj.save()
        return obj

    @classmethod
    def _make_study(
            cls, identifier, file_name, investigation, title, description,
            retraction_data=None, sharing_data=None, comments=None):
        """Create Study in database"""
        values = {
            'identifier': identifier,
            'file_name': file_name,
            'investigation': investigation,
            'title': title,
            'description': description,
            'comments': comments}
        obj = Study(**values)
        obj.save()
        return obj

    @classmethod
    def _make_protocol(
            cls, name, study, protocol_type, description, uri, version,
            parameters, components, retraction_data=None, sharing_data=None,
            comments=None):
        """Create Protocol in database"""
        values = {
            'name': name,
            'study': study,
            'protocol_type': protocol_type,
            'description': description,
            'uri': uri,
            'version': version,
            'parameters': parameters,
            'components': components,
            'comments': comments}
        obj = Protocol(**values)
        obj.save()
        return obj

    @classmethod
    def _make_assay(
            cls, file_name, study, tech_platform, tech_type, measurement_type,
            arcs, retraction_data=None, sharing_data=None, comments=None):
        """Create Assay in database"""
        # NOTE: characteristics_cat and unit_cat not currently supported
        values = {
            'file_name': file_name,
            'study': study,
            'technology_platform': tech_platform,
            'technology_type': tech_type,
            'measurement_type': measurement_type,
            'arcs': arcs,
            'comments': comments}
        obj = Assay(**values)
        obj.save()
        return obj

    @classmethod
    def _make_material(
            cls, item_type, name, unique_name, characteristics, study, assay,
            material_type, factor_values, extract_label=None,
            retraction_data=None, sharing_data=None, comments=None):
        """Create Material in database"""
        values = {
            'item_type': item_type,
            'name': name,
            'unique_name': unique_name,
            'characteristics': characteristics,
            'study': study,
            'assay': assay,
            'material_type': material_type,
            'factor_values': factor_values,
            'extract_label': extract_label,
            'comments': comments}
        obj = GenericMaterial(**values)
        obj.save()
        return obj

    @classmethod
    def _make_process(
            cls, name, unique_name, protocol, study, assay,
            parameter_values, performer, perform_date,
            retraction_data=None, sharing_data=None, comments=None):
        """Create Material in database"""
        # NOTE: array_design_ref and scan_name not supported at the moment
        values = {
            'name': name,
            'unique_name': unique_name,
            'protocol': protocol,
            'study': study,
            'assay': assay,
            'parameter_values': parameter_values,
            'performer': performer,
            'perform_date': perform_date,
            'comments': comments}
        obj = Process(**values)
        obj.save()
        return obj


# Test classes -----------------------------------------------------------------


class TestSampleSheetBase(
        TestCase, ProjectMixin, RoleAssignmentMixin, SampleSheetModelMixin):
    """Base class for Samplesheets tests"""

    def setUp(self):
        # Make owner user
        self.user_owner = self.make_user('owner')

        # Init project, role and assignment
        self.project = self._make_project(
            'TestProject', OMICS_CONSTANTS['PROJECT_TYPE_PROJECT'], None)
        self.role_owner = Role.objects.get_or_create(
            name=OMICS_CONSTANTS['PROJECT_ROLE_OWNER'])[0]
        self.assignment_owner = self._make_assignment(
            self.project, self.user_owner, self.role_owner)

        # Set up Investigation
        self.investigation = self._make_investigation(
            identifier=INV_IDENTIFIER,
            file_name=INV_FILE_NAME,
            project=self.project,
            title=INV_TITLE,
            description=DEFAULT_DESCRIPTION,
            comments=DEFAULT_COMMENTS)

        # Set up Study
        self.study = self._make_study(
            identifier=STUDY_IDENTIFIER,
            file_name=STUDY_FILE_NAME,
            investigation=self.investigation,
            title=STUDY_TITLE,
            description=DEFAULT_DESCRIPTION,
            comments=DEFAULT_COMMENTS)

        # Set up Assay
        self.assay = self._make_assay(
            file_name=ASSAY_FILE_NAME,
            study=self.study,
            tech_platform=ASSAY_TECH_PLATFORM,
            tech_type=ASSAY_TECH_TYPE,
            measurement_type=ASSAY_MEASURE_TYPE,
            arcs=[],
            comments=DEFAULT_COMMENTS)


class TestInvestigation(TestSampleSheetBase):
    """Tests for the Investigation model"""

    def test_initialization(self):
        """Test Investigation initialization"""
        expected = {
            'id': self.investigation.pk,
            'identifier': INV_IDENTIFIER,
            'file_name': INV_FILE_NAME,
            'project': self.project.pk,
            'title': INV_TITLE,
            'description': DEFAULT_DESCRIPTION,
            'ontology_source_refs': {},
            'omics_uuid': self.investigation.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS,
            'irods_status': False,
            'active': True}
        self.assertEqual(model_to_dict(self.investigation), expected)

    def test__str__(self):
        """Test Investigation __str__() function"""
        expected = '{}: {}'.format(self.project.title, INV_TITLE)
        self.assertEqual(str(self.investigation), expected)

    def test__repr__(self):
        """Test Investigation __repr__() function"""
        expected = "Investigation('{}', '{}')".format(
            self.project.title, INV_TITLE)
        self.assertEqual(repr(self.investigation), expected)

    def test_get_study(self):
        """Test Investigation get_study() function"""
        self.assertEqual(self.investigation.get_study(), None)

    def test_get_project(self):
        """Test Investigation get_project() function"""
        self.assertEqual(self.investigation.get_project(), self.project)


class TestStudy(TestSampleSheetBase):
    """Tests for the Study model"""

    def test_initialization(self):
        """Test Study initialization"""
        expected = {
            'id': self.study.pk,
            'identifier': STUDY_IDENTIFIER,
            'file_name': STUDY_FILE_NAME,
            'investigation': self.investigation.pk,
            'title': STUDY_TITLE,
            'description': DEFAULT_DESCRIPTION,
            'study_design': {},
            'factors': {},
            'characteristic_cat': {},
            'unit_cat': {},
            'arcs': [],
            'header': {},
            'omics_uuid': self.study.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.study), expected)

    def test__str__(self):
        """Test Study __str__() function"""
        expected = '{}: {}'.format(self.project.title, STUDY_TITLE)
        self.assertEqual(str(self.study), expected)

    def test__repr__(self):
        """Test Study __repr__() function"""
        expected = "Study('{}', '{}')".format(
            self.project.title, STUDY_TITLE)
        self.assertEqual(repr(self.study), expected)

    def test_get_study(self):
        """Test Study get_study() function"""
        self.assertEqual(self.study.get_study(), self.study)

    def test_get_project(self):
        """Test Study get_project() function"""
        self.assertEqual(self.study.get_project(), self.project)

    def test_get_name(self):
        """Test get_name() when title is set"""
        self.assertEqual(self.study.get_name(), self.study.title)

    def test_get_name_no_title(self):
        """Test get_name() when no title is set"""
        self.study.title = ''
        self.study.save()
        self.assertEqual(self.study.get_name(), self.study.identifier)


class TestProtocol(TestSampleSheetBase):
    """Tests for the Protocol model"""

    def setUp(self):
        super(TestProtocol, self).setUp()

        # Set up Protocol
        self.protocol = self._make_protocol(
            name=PROTOCOL_NAME,
            study=self.study,
            protocol_type=PROTOCOL_TYPE,
            description=DEFAULT_DESCRIPTION,
            uri=PROTOCOL_URI,
            version=PROTOCOL_VERSION,
            parameters=PROTOCOL_PARAMS,
            components=PROTOCOL_COMPONENTS,
            comments=DEFAULT_COMMENTS)

    def test_initialization(self):
        """Test Protocol initialization"""
        expected = {
            'id': self.protocol.pk,
            'name': PROTOCOL_NAME,
            'study': self.study.pk,
            'protocol_type': PROTOCOL_TYPE,
            'description': DEFAULT_DESCRIPTION,
            'uri': PROTOCOL_URI,
            'version': PROTOCOL_VERSION,
            'parameters': PROTOCOL_PARAMS,
            'components': PROTOCOL_COMPONENTS,
            'omics_uuid': self.protocol.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.protocol), expected)

    def test__str__(self):
        """Test Protocol __str__() function"""
        expected = '{}: {}/{}'.format(
            self.project.title, STUDY_TITLE, PROTOCOL_NAME)
        self.assertEqual(str(self.protocol), expected)

    def test__repr__(self):
        """Test Protocol __repr__() function"""
        expected = "Protocol('{}', '{}', '{}')".format(
            self.project.title, STUDY_TITLE, PROTOCOL_NAME)
        self.assertEqual(repr(self.protocol), expected)

    def test_get_study(self):
        """Test Protocol get_study() function"""
        self.assertEqual(self.protocol.get_study(), self.study)

    def test_get_project(self):
        """Test Protocol get_project() function"""
        self.assertEqual(self.protocol.get_project(), self.project)


class TestAssay(TestSampleSheetBase):
    """Tests for the Assay model"""

    def test_initialization(self):
        """Test Study initialization"""
        expected = {
            'id': self.assay.pk,
            'file_name': ASSAY_FILE_NAME,
            'study': self.study.pk,
            'technology_platform': ASSAY_TECH_PLATFORM,
            'technology_type': ASSAY_TECH_TYPE,
            'measurement_type': ASSAY_MEASURE_TYPE,
            'characteristic_cat': {},
            'unit_cat': {},
            'arcs': [],
            'header': {},
            'omics_uuid': self.assay.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.assay), expected)

    def test__str__(self):
        """Test Assay __str__() function"""
        expected = '{}: {}/{}'.format(
            self.project.title, STUDY_TITLE, self.assay.get_name())
        self.assertEqual(str(self.assay), expected)

    def test__repr__(self):
        """Test Assay __repr__() function"""
        expected = "Assay('{}', '{}', '{}')".format(
            self.project.title, STUDY_TITLE, self.assay.get_name())
        self.assertEqual(repr(self.assay), expected)

    def test_get_study(self):
        """Test Assay get_study() function"""
        self.assertEqual(self.assay.get_study(), self.study)

    def test_get_project(self):
        """Test Assay get_project() function"""
        self.assertEqual(self.assay.get_project(), self.project)

    def test_get_name(self):
        """Test Assay get_name() function"""
        self.assertEqual(self.assay.get_name(), 'assay')


class TestSource(TestSampleSheetBase):
    """Tests for the GenericMaterial model with type SOURCE"""

    def setUp(self):
        super(TestSource, self).setUp()

        # Set up SOURCE GenericMaterial
        self.material = self._make_material(
            item_type='SOURCE',
            name=SOURCE_NAME,
            unique_name=SOURCE_UNIQUE_NAME,
            characteristics=SOURCE_CHARACTERISTICS,
            study=self.study,
            assay=None,
            material_type=None,
            factor_values=None,
            extract_label=None,
            comments=DEFAULT_COMMENTS)

    def test_initialization(self):
        """Test SOURCE GenericMaterial initialization"""
        expected = {
            'id': self.material.pk,
            'item_type': 'SOURCE',
            'name': SOURCE_NAME,
            'unique_name': SOURCE_UNIQUE_NAME,
            'characteristics': SOURCE_CHARACTERISTICS,
            'study': self.study.pk,
            'assay': None,
            'material_type': None,
            'factor_values': None,
            'extract_label': None,
            'omics_uuid': self.material.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.material), expected)

    def test__str__(self):
        """Test SOURCE GenericMaterial __str__() function"""
        expected = '{}: {}/{}/{}/{}'.format(
            self.project.title, STUDY_TITLE, NOT_AVAILABLE_STR, 'SOURCE',
            SOURCE_UNIQUE_NAME)
        self.assertEqual(str(self.material), expected)

    def test__repr__(self):
        """Test SOURCE GenericMaterial __repr__() function"""
        expected = "GenericMaterial('{}', '{}', '{}', '{}', '{}')".format(
            self.project.title, STUDY_TITLE, NOT_AVAILABLE_STR, 'SOURCE',
            SOURCE_UNIQUE_NAME)
        self.assertEqual(repr(self.material), expected)

    def test_get_study(self):
        """Test SOURCE GenericMaterial get_study() function"""
        self.assertEqual(self.material.get_study(), self.study)

    def test_get_project(self):
        """Test SOURCE GenericMaterial get_project() function"""
        self.assertEqual(self.material.get_project(), self.project)

    def test_get_parent(self):
        """Test SOURCE GenericMaterial get_parent() function"""
        self.assertEqual(self.material.get_parent(), self.study)


class TestSample(TestSampleSheetBase):
    """Tests for the GenericMaterial model with type SAMPLE"""

    def setUp(self):
        super(TestSample, self).setUp()

        # Set up SAMPLE GenericMaterial
        self.material = self._make_material(
            item_type='SAMPLE',
            name=SAMPLE_NAME,
            unique_name=SAMPLE_UNIQUE_NAME,
            characteristics=SAMPLE_CHARACTERISTICS,
            study=self.study,
            assay=None,
            material_type=None,
            factor_values=None,     # TODO: Test this
            extract_label=None,     # TODO: Test this
            comments=DEFAULT_COMMENTS)

    def test_initialization(self):
        """Test SAMPLE GenericMaterial initialization"""
        expected = {
            'id': self.material.pk,
            'item_type': 'SAMPLE',
            'name': SAMPLE_NAME,
            'unique_name': SAMPLE_UNIQUE_NAME,
            'characteristics': SAMPLE_CHARACTERISTICS,
            'study': self.study.pk,
            'assay': None,
            'material_type': None,
            'factor_values': None,
            'extract_label': None,
            'omics_uuid': self.material.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.material), expected)

    def test__str__(self):
        """Test SAMPLE GenericMaterial __str__() function"""
        expected = '{}: {}/{}/{}/{}'.format(
            self.project.title, STUDY_TITLE, NOT_AVAILABLE_STR, 'SAMPLE',
            SAMPLE_UNIQUE_NAME)
        self.assertEqual(str(self.material), expected)

    def test__repr__(self):
        """Test SAMPLE GenericMaterial __repr__() function"""
        expected = "GenericMaterial('{}', '{}', '{}', '{}', '{}')".format(
            self.project.title, STUDY_TITLE, NOT_AVAILABLE_STR, 'SAMPLE',
            SAMPLE_UNIQUE_NAME)
        self.assertEqual(repr(self.material), expected)

    def test_get_study(self):
        """Test SAMPLE GenericMaterial get_study() function"""
        self.assertEqual(self.material.get_study(), self.study)

    def test_get_project(self):
        """Test SAMPLE GenericMaterial get_project() function"""
        self.assertEqual(self.material.get_project(), self.project)

    def test_get_parent(self):
        """Test SAMPLE GenericMaterial get_parent() function"""
        self.assertEqual(self.material.get_parent(), self.study)


class TestMaterial(TestSampleSheetBase):
    """Tests for the GenericMaterial model with type MATERIAL"""

    def setUp(self):
        super(TestMaterial, self).setUp()

        # Set up MATERIAL GenericMaterial
        self.material = self._make_material(
            item_type='MATERIAL',
            name=MATERIAL_NAME,
            unique_name=MATERIAL_UNIQUE_NAME,
            characteristics={},
            study=self.study,
            assay=self.assay,
            material_type=MATERIAL_TYPE,
            factor_values=None,
            extract_label=None,
            comments=DEFAULT_COMMENTS)

    def test_initialization(self):
        """Test MATERIAL GenericMaterial initialization"""
        expected = {
            'id': self.material.pk,
            'item_type': 'MATERIAL',
            'name': MATERIAL_NAME,
            'unique_name': MATERIAL_UNIQUE_NAME,
            'characteristics': {},
            'study': self.study.pk,
            'assay': self.assay.pk,
            'material_type': MATERIAL_TYPE,
            'factor_values': None,
            'extract_label': None,
            'omics_uuid': self.material.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.material), expected)

    def test__str__(self):
        """Test MATERIAL GenericMaterial __str__() function"""
        expected = '{}: {}/{}/{}/{}'.format(
            self.project.title, STUDY_TITLE, self.assay.get_name(), 'MATERIAL',
            MATERIAL_UNIQUE_NAME)
        self.assertEqual(str(self.material), expected)

    def test__repr__(self):
        """Test MATERIAL GenericMaterial __repr__() function"""
        expected = "GenericMaterial('{}', '{}', '{}', '{}', '{}')".format(
            self.project.title, STUDY_TITLE, self.assay.get_name(), 'MATERIAL',
            MATERIAL_UNIQUE_NAME)
        self.assertEqual(repr(self.material), expected)

    def test_get_study(self):
        """Test MATERIAL GenericMaterial get_study() function"""
        self.assertEqual(self.material.get_study(), self.study)

    def test_get_project(self):
        """Test MATERIAL GenericMaterial get_project() function"""
        self.assertEqual(self.material.get_project(), self.project)

    def test_get_parent(self):
        """Test MATERIAL GenericMaterial get_parent() function"""
        self.assertEqual(self.material.get_parent(), self.assay)


class TestDataFile(TestSampleSheetBase):
    """Tests for the GenericMaterial model with type DATA"""

    def setUp(self):
        super(TestDataFile, self).setUp()

        # Set up DATA GenericMaterial
        self.material = self._make_material(
            item_type='DATA',
            name=DATA_NAME,
            unique_name=DATA_UNIQUE_NAME,
            characteristics={},
            study=self.study,
            assay=self.assay,
            material_type=DATA_TYPE,
            factor_values=None,
            extract_label=None,
            comments=DEFAULT_COMMENTS)

    def test_initialization(self):
        """Test MATERIAL GenericMaterial initialization"""
        expected = {
            'id': self.material.pk,
            'item_type': 'DATA',
            'name': DATA_NAME,
            'unique_name': DATA_UNIQUE_NAME,
            'characteristics': {},
            'study': self.study.pk,
            'assay': self.assay.pk,
            'material_type': DATA_TYPE,
            'factor_values': None,
            'extract_label': None,
            'omics_uuid': self.material.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.material), expected)

    def test__str__(self):
        """Test DATA GenericMaterial __str__() function"""
        expected = '{}: {}/{}/{}/{}'.format(
            self.project.title, STUDY_TITLE, self.assay.get_name(), 'DATA',
            DATA_UNIQUE_NAME)
        self.assertEqual(str(self.material), expected)

    def test__repr__(self):
        """Test DATA GenericMaterial __repr__() function"""
        expected = "GenericMaterial('{}', '{}', '{}', '{}', '{}')".format(
            self.project.title, STUDY_TITLE, self.assay.get_name(), 'DATA',
            DATA_UNIQUE_NAME)
        self.assertEqual(repr(self.material), expected)

    def test_get_study(self):
        """Test DATA GenericMaterial get_study() function"""
        self.assertEqual(self.material.get_study(), self.study)

    def test_get_project(self):
        """Test DATA GenericMaterial get_project() function"""
        self.assertEqual(self.material.get_project(), self.project)

    def test_get_parent(self):
        """Test DATA GenericMaterial get_parent() function"""
        self.assertEqual(self.material.get_parent(), self.assay)


class TestProcess(TestSampleSheetBase):
    """Tests for the Process model"""

    def setUp(self):
        super(TestProcess, self).setUp()

        # Set up Protocol
        self.protocol = self._make_protocol(
            name=PROTOCOL_NAME,
            study=self.study,
            protocol_type=PROTOCOL_TYPE,
            description=DEFAULT_DESCRIPTION,
            uri=PROTOCOL_URI,
            version=PROTOCOL_VERSION,
            parameters=PROTOCOL_PARAMS,
            components=PROTOCOL_COMPONENTS,
            comments=DEFAULT_COMMENTS)

        # Set up Process
        self.process = self._make_process(
            name=PROCESS_NAME,
            unique_name=PROCESS_UNIQUE_NAME,
            protocol=self.protocol,
            study=self.study,
            assay=self.assay,
            parameter_values=PROCESS_PARAM_VALUES,
            performer=PROCESS_PERFORMER,
            perform_date=PROCESS_PERFORM_DATE,
            comments=DEFAULT_COMMENTS)

    def test_initialization(self):
        """Test Process initialization"""
        expected = {
            'id': self.process.pk,
            'name': PROCESS_NAME,
            'unique_name': PROCESS_UNIQUE_NAME,
            'protocol': self.protocol.pk,
            'study': self.study.pk,
            'assay': self.assay.pk,
            'parameter_values': PROCESS_PARAM_VALUES,
            'performer': PROCESS_PERFORMER,
            'perform_date': PROCESS_PERFORM_DATE,
            'array_design_ref': None,
            'scan_name': None,
            'omics_uuid': self.process.omics_uuid,
            'sharing_data': {},
            'retraction_data': {},
            'comments': DEFAULT_COMMENTS}
        self.assertEqual(model_to_dict(self.process), expected)

    def test__str__(self):
        """Test Process __str__() function"""
        expected = '{}: {}/{}/{}'.format(
            self.project.title, STUDY_TITLE, self.assay.get_name(),
            PROCESS_UNIQUE_NAME)
        self.assertEqual(str(self.process), expected)

    def test__repr__(self):
        """Test Process __repr__() function"""
        expected = "Process('{}', '{}', '{}', '{}')".format(
            self.project.title, STUDY_TITLE, self.assay.get_name(),
            PROCESS_UNIQUE_NAME)
        self.assertEqual(repr(self.process), expected)

    def test_get_study(self):
        """Test Process get_study() function"""
        self.assertEqual(self.process.get_study(), self.study)

    def test_get_project(self):
        """Test Process get_project() function"""
        self.assertEqual(self.process.get_project(), self.project)

    def test_get_parent(self):
        """Test Process get_parent() function"""
        self.assertEqual(self.process.get_parent(), self.assay)
