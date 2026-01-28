from odoo import models, fields, api
from datetime import timedelta

class ChamCong(models.Model):
    _name = 'cham_cong'
    _description = 'Chấm công hàng ngày'
    _order = 'ngay desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay = fields.Date("Ngày", default=fields.Date.context_today, required=True)
    gio_vao = fields.Datetime("Giờ vào")
    gio_ra = fields.Datetime("Giờ ra")
    
    so_gio_lam = fields.Float("Số giờ làm", compute="_compute_details", store=True)
    ot_hours = fields.Float("Giờ OT", compute="_compute_details", store=True)
    di_muon_ve_som = fields.Boolean("Đi muộn/Về sớm", compute="_compute_details", store=True)
    so_cong = fields.Float("Số công", compute="_compute_details", store=True)

    @api.depends('gio_vao', 'gio_ra')
    def _compute_details(self):
        for record in self:
            if record.gio_vao and record.gio_ra:
                diff = record.gio_ra - record.gio_vao
                hours = diff.total_seconds() / 3600
                record.so_gio_lam = hours
                
                # Logic chuẩn: 8 tiếng = 1 công
                if hours >= 8:
                    record.so_cong = 1.0
                    record.ot_hours = hours - 8
                    record.di_muon_ve_som = False
                else:
                    record.so_cong = hours / 8
                    record.ot_hours = 0
                    record.di_muon_ve_som = True
            else:
                record.so_gio_lam = record.so_cong = record.ot_hours = 0
                record.di_muon_ve_som = False