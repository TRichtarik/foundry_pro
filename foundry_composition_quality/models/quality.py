from odoo import api, fields, models


class QualityPoint(models.Model):
    _inherit = 'quality.point'

    heat_required = fields.Boolean(
        string='Require Heat',
        help='Only create checks for MOs that have a linked heat.',
    )


class QualityCheck(models.Model):
    _inherit = 'quality.check'

    analysis_id = fields.Many2one(
        'foundry.analysis', string='Chemistry Analysis',
        readonly=True,
    )

    def action_open_chemistry_wizard(self):
        """Open the foundry.analysis form for this chemistry check.

        Pre-fills heat from the linked MO and creates an analysis record
        if one does not yet exist.
        """
        self.ensure_one()
        heat = self._get_heat_for_check()
        if not self.analysis_id and heat:
            analysis = self.env['foundry.analysis'].create({
                'heat_id': heat.id,
                'sample_point': 'furnace',
            })
            self.analysis_id = analysis
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Chemistry Sample',
            'res_model': 'foundry.analysis',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'foundry_quality_check_id': self.id,
            },
        }
        if self.analysis_id:
            action['res_id'] = self.analysis_id.id
        elif heat:
            action['context']['default_heat_id'] = heat.id
        return action

    def action_confirm_chemistry(self):
        """Called after analysis is saved to pass/fail the check."""
        self.ensure_one()
        if self.analysis_id and self.analysis_id.in_spec:
            self.do_pass()
        elif self.analysis_id:
            self.do_fail()

    def _get_heat_for_check(self):
        """Find the heat linked to this check's production order."""
        if self.production_id and self.production_id.heat_ids:
            return self.production_id.heat_ids[:1]
        return self.env['foundry.heat']

    def action_open_quality_check_wizard(self, current_check_id=None):
        """Override to redirect chemistry_sample checks to our wizard."""
        check = self.browse(current_check_id) if current_check_id else self[:1]
        if check and check.test_type == 'chemistry_sample':
            return check.action_open_chemistry_wizard()
        return super().action_open_quality_check_wizard(current_check_id=current_check_id)


class FoundryAnalysis(models.Model):
    _inherit = 'foundry.analysis'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        ctx_check_id = self.env.context.get('foundry_quality_check_id')
        if ctx_check_id:
            check = self.env['quality.check'].browse(ctx_check_id).exists()
            if check and len(records) == 1:
                check.analysis_id = records
                check.action_confirm_chemistry()
        return records

    def write(self, vals):
        res = super().write(vals)
        for analysis in self:
            check = self.env['quality.check'].search([
                ('analysis_id', '=', analysis.id),
                ('quality_state', '=', 'none'),
            ], limit=1)
            if check:
                check.action_confirm_chemistry()
        return res
