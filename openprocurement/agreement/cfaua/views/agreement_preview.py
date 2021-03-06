# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    json_view,
    APIResource,
    context_unpack
)
from openprocurement.agreement.core.resource import agreements_resource
from openprocurement.agreement.cfaua.utils import apply_modifications


@agreements_resource(name='cfaua.AgreementPreview',
                     path='/agreements/{agreement_id}/preview',
                     agreementType='cfaua',
                     description='Agreements resource')
class AgreementPreviewResource(APIResource):

    @json_view(permission='view_agreement')
    def get(self):
        if not self.context.changes or self.context.changes[-1]['status'] != 'pending':
            return {"data": self.context.serialize("view")}
        # save=True mean apply modifications directy for context not context copy
        warnings = apply_modifications(self.request, self.context, save=True)
        response_data = {'data': self.context.serialize('view')}
        if warnings:
            response_data['warnings'] = warnings
            self.LOGGER.info('warnings: {}'.format(warnings),
                             extra=context_unpack(self.request, {'MESSAGE_ID': 'agreement_preview'}))
        return response_data
