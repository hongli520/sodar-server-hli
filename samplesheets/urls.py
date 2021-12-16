from django.conf.urls import url

import samplesheets.views_ajax
import samplesheets.views_api
import samplesheets.views_taskflow
from samplesheets import views


app_name = 'samplesheets'

# UI views
urls_ui = [
    url(
        regex=r'^(?P<project>[0-9a-f-]+)$',
        view=views.ProjectSheetsView.as_view(),
        name='project_sheets',
    ),
    url(
        regex=r'^import/(?P<project>[0-9a-f-]+)$',
        view=views.SheetImportView.as_view(),
        name='import',
    ),
    url(
        regex=r'^sync/(?P<project>[0-9a-f-]+)$',
        view=views.SheetRemoteSyncView.as_view(),
        name='sync',
    ),
    url(
        regex=r'^template/select/(?P<project>[0-9a-f-]+)$',
        view=views.SheetTemplateSelectView.as_view(),
        name='template_select',
    ),
    url(
        regex=r'^template/create/(?P<project>[0-9a-f-]+)$',
        view=views.SheetTemplateCreateFormView.as_view(),
        name='template_create',
    ),
    url(
        regex=r'^export/excel/study/(?P<study>[0-9a-f-]+)$',
        view=views.SheetExcelExportView.as_view(),
        name='export_excel',
    ),
    url(
        regex=r'^export/excel/assay/(?P<assay>[0-9a-f-]+)$',
        view=views.SheetExcelExportView.as_view(),
        name='export_excel',
    ),
    url(
        regex=r'^export/isa/(?P<project>[0-9a-f-]+)$',
        view=views.SheetISAExportView.as_view(),
        name='export_isa',
    ),
    url(
        regex=r'^export/version/(?P<isatab>[0-9a-f-]+)$',
        view=views.SheetISAExportView.as_view(),
        name='export_isa',
    ),
    url(
        regex=r'^collections/(?P<project>[0-9a-f-]+)$',
        view=views.IrodsCollsCreateView.as_view(),
        name='collections',
    ),
    url(
        regex=r'^delete/(?P<project>[0-9a-f-]+)$',
        view=views.SheetDeleteView.as_view(),
        name='delete',
    ),
    url(
        regex=r'^cache/update/(?P<project>[0-9a-f-]+)$',
        view=views.SheetCacheUpdateView.as_view(),
        name='cache_update',
    ),
    url(
        regex=r'^versions/(?P<project>[0-9a-f-]+)$',
        view=views.SheetVersionListView.as_view(),
        name='versions',
    ),
    url(
        regex=r'^version/restore/(?P<isatab>[0-9a-f-]+)$',
        view=views.SheetVersionRestoreView.as_view(),
        name='version_restore',
    ),
    url(
        regex=r'^version/compare/(?P<project>[0-9a-f-]+)$',
        view=views.SheetVersionCompareView.as_view(),
        name='version_compare',
    ),
    url(
        regex=r'^version/compare/file/(?P<project>[0-9a-f-]+)$',
        view=views.SheetVersionCompareFileView.as_view(),
        name='version_compare_file',
    ),
    url(
        regex=r'^version/update/(?P<isatab>[0-9a-f-]+)$',
        view=views.SheetVersionUpdateView.as_view(),
        name='version_update',
    ),
    url(
        regex=r'^version/delete/(?P<isatab>[0-9a-f-]+)$',
        view=views.SheetVersionDeleteView.as_view(),
        name='version_delete',
    ),
    url(
        regex=r'^version/delete/batch/(?P<project>[0-9a-f-]+)$',
        view=views.SheetVersionDeleteBatchView.as_view(),
        name='version_delete_batch',
    ),
    url(
        regex=r'^irods/tickets/(?P<project>[0-9a-f-]+)$',
        view=views.IrodsAccessTicketListView.as_view(),
        name='irods_tickets',
    ),
    url(
        regex=r'^irods/ticket/create/(?P<project>[0-9a-f-]+)$',
        view=views.IrodsAccessTicketCreateView.as_view(),
        name='irods_ticket_create',
    ),
    url(
        regex=r'^irods/ticket/update/(?P<irodsaccessticket>[0-9a-f-]+)$',
        view=views.IrodsAccessTicketUpdateView.as_view(),
        name='irods_ticket_update',
    ),
    url(
        regex=r'^irods/ticket/delete/(?P<irodsaccessticket>[0-9a-f-]+)$',
        view=views.IrodsAccessTicketDeleteView.as_view(),
        name='irods_ticket_delete',
    ),
    url(
        regex=r'^irods/requests/(?P<project>[0-9a-f-]+)$',
        view=views.IrodsDataRequestListView.as_view(),
        name='irods_requests',
    ),
    url(
        regex=r'^irods/request/create/(?P<project>[0-9a-f-]+)$',
        view=views.IrodsRequestCreateView.as_view(),
        name='irods_request_create',
    ),
    url(
        regex=r'^irods/request/update/(?P<irodsdatarequest>[0-9a-f-]+)$',
        view=views.IrodsRequestUpdateView.as_view(),
        name='irods_request_update',
    ),
    url(
        regex=r'^irods/request/delete/(?P<irodsdatarequest>[0-9a-f-]+)$',
        view=views.IrodsRequestDeleteView.as_view(),
        name='irods_request_delete',
    ),
    url(
        regex=r'^irods/request/accept/(?P<irodsdatarequest>[0-9a-f-]+)$',
        view=views.IrodsRequestAcceptView.as_view(),
        name='irods_request_accept',
    ),
    url(
        regex=r'^irods/request/reject/(?P<irodsdatarequest>[0-9a-f-]+)$',
        view=views.IrodsRequestRejectView.as_view(),
        name='irods_request_reject',
    ),
]

# REST API views
urls_api = [
    url(
        regex=r'^api/investigation/retrieve/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_api.InvestigationRetrieveAPIView.as_view(),
        name='api_investigation_retrieve',
    ),
    url(
        regex=r'^api/irods/collections/create/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_api.IrodsCollsCreateAPIView.as_view(),
        name='api_irods_colls_create',
    ),
    url(
        regex=r'^api/import/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_api.SheetImportAPIView.as_view(),
        name='api_import',
    ),
    url(
        regex=r'^api/export/zip/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_api.SheetISAExportAPIView.as_view(),
        name='api_export_zip',
    ),
    url(
        regex=r'^api/export/json/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_api.SheetISAExportAPIView.as_view(),
        name='api_export_json',
    ),
    url(
        regex=r'^api/file/exists$',
        view=samplesheets.views_api.SampleDataFileExistsAPIView.as_view(),
        name='api_file_exists',
    ),
    url(
        regex=r'^api/remote/get/(?P<project>[0-9a-f-]+)/(?P<secret>[\w\-]+)$',
        view=samplesheets.views_api.RemoteSheetGetAPIView.as_view(),
        name='api_remote_get',
    ),
]

# Ajax API views
urls_ajax = [
    url(
        regex=r'^ajax/context/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetContextAjaxView.as_view(),
        name='ajax_context',
    ),
    url(
        regex=r'^ajax/study/tables/(?P<study>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.StudyTablesAjaxView.as_view(),
        name='ajax_study_tables',
    ),
    url(
        regex=r'^ajax/study/links/(?P<study>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.StudyLinksAjaxView.as_view(),
        name='ajax_study_links',
    ),
    url(
        regex=r'^ajax/warnings/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetWarningsAjaxView.as_view(),
        name='ajax_warnings',
    ),
    url(
        regex=r'^ajax/edit/cell/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetCellEditAjaxView.as_view(),
        name='ajax_edit_cell',
    ),
    url(
        regex=r'^ajax/edit/row/insert/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetRowInsertAjaxView.as_view(),
        name='ajax_edit_row_insert',
    ),
    url(
        regex=r'^ajax/edit/row/delete/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetRowDeleteAjaxView.as_view(),
        name='ajax_edit_row_delete',
    ),
    url(
        regex=r'^ajax/version/save/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetVersionSaveAjaxView.as_view(),
        name='ajax_version_save',
    ),
    url(
        regex=r'^ajax/edit/finish/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetEditFinishAjaxView.as_view(),
        name='ajax_edit_finish',
    ),
    url(
        regex=r'^ajax/config/update/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetEditConfigAjaxView.as_view(),
        name='ajax_config_update',
    ),
    url(
        regex=r'^ajax/display/update/(?P<study>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.StudyDisplayConfigAjaxView.as_view(),
        name='ajax_display_update',
    ),
    url(
        regex=r'^ajax/irods/request/create/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.IrodsRequestCreateAjaxView.as_view(),
        name='ajax_irods_request_create',
    ),
    url(
        regex=r'^ajax/irods/request/delete/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.IrodsRequestDeleteAjaxView.as_view(),
        name='ajax_irods_request_delete',
    ),
    url(
        regex=r'^ajax/irods/objects/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.IrodsObjectListAjaxView.as_view(),
        name='ajax_irods_objects',
    ),
    url(
        regex=r'^ajax/version/compare/(?P<project>[0-9a-f-]+)$',
        view=samplesheets.views_ajax.SheetVersionCompareAjaxView.as_view(),
        name='ajax_version_compare',
    ),
]

# Taskflow API views
urls_taskflow = [
    url(
        regex=r'^taskflow/dirs/get$',
        view=samplesheets.views_taskflow.TaskflowCollStatusGetAPIView.as_view(),
        name='taskflow_sheet_colls_get',
    ),
    url(
        regex=r'^taskflow/dirs/set$',
        view=samplesheets.views_taskflow.TaskflowCollStatusSetAPIView.as_view(),
        name='taskflow_sheet_colls_set',
    ),
    url(
        regex=r'^taskflow/delete$',
        view=samplesheets.views_taskflow.TaskflowSheetDeleteAPIView.as_view(),
        name='taskflow_sheet_delete',
    ),
]

urlpatterns = urls_ui + urls_api + urls_ajax + urls_taskflow
