from lxml import etree

# Load XML
tree = etree.parse("quanlybanan.xml")
root = tree.getroot()

# 1. Lấy tất cả bàn
ban_list = root.xpath("//BAN/TENBAN")
print("Tất cả bàn:", [ban.text for ban in ban_list])

# 2. Lấy tất cả nhân viên
nhanvien_list = root.xpath("//NHANVIEN/TENV")
print("Tất cả nhân viên:", [nv.text for nv in nhanvien_list])

# 3. Lấy tất cả tên món
mon_list = root.xpath("//MON/TENMON")
print("Tất cả tên món:", [mon.text for mon in mon_list])

# 4. Lấy tên nhân viên có mã NV02
ten_nv02 = root.xpath("//NHANVIEN[MANV='NV02']/TENV")[0].text
print("Tên nhân viên NV02:", ten_nv02)

# 5. Lấy tên và số điện thoại của nhân viên NV03
nv03 = root.xpath("//NHANVIEN[MANV='NV03']")[0]
print("Tên và SĐT NV03:", nv03.findtext("TENV"), nv03.findtext("SDT"))

# 6. Lấy tên món có giá > 50,000
mon_gia_cao = root.xpath("//MON[GIA>50000]/TENMON")
print("Món giá > 50,000:", [mon.text for mon in mon_gia_cao])

# 7. Lấy số bàn của hóa đơn HD03
soban_hd03 = root.xpath("//HOADON[SOHD='HD03']/SOBAN")[0].text
print("Số bàn HD03:", soban_hd03)

# 8. Lấy tên món có mã M02
tenmon_m02 = root.xpath("//MON[MAMON='M02']/TENMON")[0].text
print("Tên món M02:", tenmon_m02)

# 9. Lấy ngày lập của hóa đơn HD03
ngaylap_hd03 = root.xpath("//HOADON[SOHD='HD03']/NGAYLAP")[0].text
print("Ngày lập HD03:", ngaylap_hd03)

# 10. Lấy tất cả mã món trong hóa đơn HD01
ma_mon_hd01 = root.xpath("//HOADON[SOHD='HD01']//CTHD/MAMON")
print("Mã món HD01:", [m.text for m in ma_mon_hd01])

# 11. Lấy tên món trong hóa đơn HD01
ten_mon_hd01 = [root.xpath(f"//MON[MAMON='{m.text}']/TENMON")[0].text for m in ma_mon_hd01]
print("Tên món HD01:", ten_mon_hd01)

# 12. Lấy tên nhân viên lập hóa đơn HD02
manv_hd02 = root.xpath("//HOADON[SOHD='HD02']/MANV")[0].text
ten_nv_hd02 = root.xpath(f"//NHANVIEN[MANV='{manv_hd02}']/TENV")[0].text
print("Tên nhân viên lập HD02:", ten_nv_hd02)

# 13. Đếm số bàn
so_ban = len(root.xpath("//BAN"))
print("Số bàn:", so_ban)

# 14. Đếm số hóa đơn lập bởi NV01
so_hd_nv01 = len(root.xpath("//HOADON[MANV='NV01']"))
print("Số hóa đơn NV01:", so_hd_nv01)

# 15. Lấy tên tất cả món có trong hóa đơn của bàn số 2
ma_mon_ban2 = root.xpath("//HOADON[SOBAN='2']//CTHD/MAMON")
ten_mon_ban2 = [root.xpath(f"//MON[MAMON='{m.text}']/TENMON")[0].text for m in ma_mon_ban2]
print("Tên món bàn số 2:", ten_mon_ban2)

# 16. Lấy tất cả nhân viên từng lập hóa đơn cho bàn số 3
manv_ban3 = root.xpath("//HOADON[SOBAN='3']/MANV")
tennv_ban3 = list({root.xpath(f"//NHANVIEN[MANV='{m.text}']/TENV")[0].text for m in manv_ban3})
print("Nhân viên phục vụ bàn 3:", tennv_ban3)

# 17. Lấy tất cả hóa đơn mà nhân viên nữ lập
hd_nu = root.xpath("//HOADON[MANV=//NHANVIEN[GIOITINH='Nữ']/MANV]/SOHD")
print("Hóa đơn nhân viên nữ lập:", [h.text for h in hd_nu])

# 18. Lấy tất cả nhân viên từng phục vụ bàn số 1
manv_ban1 = root.xpath("//HOADON[SOBAN='1']/MANV")
tennv_ban1 = list({root.xpath(f"//NHANVIEN[MANV='{m.text}']/TENV")[0].text for m in manv_ban1})
print("Nhân viên phục vụ bàn 1:", tennv_ban1)

# 19. Lấy tất cả món được gọi nhiều hơn 1 lần trong các hóa đơn
from collections import defaultdict
mon_counter = defaultdict(int)
for cthd in root.xpath("//CTHD"):
    mamon = cthd.findtext("MAMON")
    soluong = int(cthd.findtext("SOLUONG"))
    mon_counter[mamon] += soluong
mon_nhieu = [m for m, sl in mon_counter.items() if sl > 1]
ten_mon_nhieu = [root.xpath(f"//MON[MAMON='{m}']/TENMON")[0].text for m in mon_nhieu]
print("Món gọi >1 lần:", ten_mon_nhieu)

# 20. Lấy tên bàn + ngày lập hóa đơn tương ứng SOHD='HD02'
hd02 = root.xpath("//HOADON[SOHD='HD02']")[0]
soban = hd02.findtext("SOBAN")
ngaylap = hd02.findtext("NGAYLAP")
tenban = root.xpath(f"//BAN[SOBAN='{soban}']/TENBAN")[0].text
print("Tên bàn + ngày lập HD02:", tenban, ngaylap)