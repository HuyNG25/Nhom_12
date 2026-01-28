from odoo import models, fields, api

class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng tính lương tháng'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    thang = fields.Selection([
        ('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),
        ('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12')
    ], string="Tháng", required=True)
    nam = fields.Integer("Năm", default=2024, required=True)
    
    luong_co_ban = fields.Float(related='nhan_vien_id.luong_co_ban', string="Lương cơ bản (Gốc)")
    tong_cong = fields.Float("Tổng công trong tháng", compute="_compute_luong", store=True)
    tong_ot = fields.Float("Tổng giờ OT", compute="_compute_luong", store=True)
    phu_cap = fields.Float(related='nhan_vien_id.phu_cap', store=True)
    
    phat = fields.Float("Tiền phạt (Đi muộn/Về sớm)", default=0)
    thuong = fields.Float("Thưởng", default=0)
    tong_luong = fields.Float("Tổng lương thực nhận", compute="_compute_luong", store=True)

    @api.depends('nhan_vien_id', 'thang', 'nam', 'phat', 'thuong')
    def _compute_luong(self):
        for record in self:
            # Tìm dữ liệu chấm công của nhân viên trong tháng/năm đó
            attendances = self.env['cham_cong'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                # Thêm filter ngày bắt đầu/kết thúc tháng ở đây nếu cần chính xác tuyệt đối
            ])
            
            # Lọc theo tháng/năm từ trường 'ngay'
            monthly_data = attendances.filtered(lambda x: str(x.ngay.month) == record.thang and x.ngay.year == record.nam)
            
            record.tong_cong = sum(monthly_data.mapped('so_cong'))
            record.tong_ot = sum(monthly_data.mapped('ot_hours'))
            
            # Công thức tính
            luong_ngay = record.luong_co_ban / 26
            tien_cong = luong_ngay * record.tong_cong
            tien_ot = record.tong_ot * (luong_ngay / 8) * 1.5 # OT x1.5
            
            record.tong_luong = tien_cong + tien_ot + record.phu_cap + record.thuong - record.phat