using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using TuanStore.Models;
using System.Net;
using PagedList;
using PagedList.Mvc;
using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.EntityFramework;
using Microsoft.Owin.Security;
using System.IO;
using Microsoft.VisualBasic.FileIO;


namespace TuanStore.Controllers
{
    public class AdminController : Controller
    {
        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        // GET: Admin
        public ActionResult Index()
        {   
            
            Entities db = new Entities();
            ViewBag.SoBinhLuan = db.BinhLuans.Count<BinhLuan>();
            DonhangKHModel donhangKH = new DonhangKHModel();
            var s = donhangKH.ThongKeDoanhThu(null,null).ToList();
            //ViewBag.DoanhThu = donhangKH.Sum(item => item.);
            
            //ViewBag.SoNguoiDangKy = (from p in db.AspNetUsers 
            //                         join q in db.AspNetRoles on p.Id equals q. )
            return View();
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult SanPham()
        {
            SanPhamModel spm = new SanPhamModel();
            ViewBag.HangSX = new SelectList(spm.GetAllHangSX(), "HangSX", "TenHang");
            ViewBag.LoaiSP = new SelectList(spm.GetAllLoaiSP(), "MaLoai", "TenLoai");
            return View();
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult EditSP(string id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            SanPhamModel spm = new SanPhamModel();
            SanPham sp = spm.FindById(id);
            if (sp == null)
            {
                return HttpNotFound();
            }
            ViewBag.HangSX = new SelectList(spm.GetAllHangSX().ToList(), "HangSX", "TenHang", sp.HangSX);
            ViewBag.LoaiSP = new SelectList(spm.GetAllLoaiSP().ToList(), "MaLoai", "TenLoai", sp.LoaiSP);
            return View(sp);
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult EditSP([Bind(Include = "MaSP,TenSP,LoaiSP,HangSX,XuatXu,GiaGoc,MoTa,SoLuong,isnew,ishot,GioiThieu,ThongSoKyThuat")] SanPham sanpham, HttpPostedFileBase ad, HttpPostedFileBase an, HttpPostedFileBase ak)
        {
            SanPhamModel spm = new SanPhamModel();
            if (ModelState.IsValid)
            {
                spm.EditSP(sanpham);
                UploadAnh(ad,sanpham.MaSP + "1");
                UploadAnh(an, sanpham.MaSP + "2");
                UploadAnh(ak, sanpham.MaSP + "3");
                return RedirectToAction("SanPham");
            }
            ViewBag.HangSX = new SelectList(spm.GetAllHangSX(), "HangSX", "TenHang", sanpham.HangSX);
            ViewBag.LoaiSP = new SelectList(spm.GetAllLoaiSP(), "MaLoai", "TenLoai", sanpham.LoaiSP);            
            return View(sanpham);
        }

        [AuthLog(Roles = "Quản trị viên")]
        public ActionResult DeleteSP(string id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            SanPhamModel spm = new SanPhamModel();
            DeleteAnh(spm.FindById(id).AnhDaiDien);
            DeleteAnh(spm.FindById(id).AnhNen);
            DeleteAnh(spm.FindById(id).AnhKhac);
            spm.DeleteSP(id);
            return TimSP(null,null,null);
        }
        public ActionResult DeleteSPByName(string name)
        {
            if (name == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            SanPhamModel spm = new SanPhamModel();
            DeleteAnh(spm.FindById(name).AnhDaiDien);
            DeleteAnh(spm.FindById(name).AnhNen);
            DeleteAnh(spm.FindById(name).AnhKhac);
            spm.DeleteSP(name);
            return RedirectToAction("SanPham");
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public bool UploadAnh(HttpPostedFileBase file,string tenfile)
        {
            // Verify that the user selected a file
            if (file != null && file.ContentLength > 0)
            {
                var name = Path.GetExtension(file.FileName);
                // extract only the filename
                if (!Path.GetExtension(file.FileName).Equals(".jpg"))
                {
                    return false;
                }
                // store the file inside ~/App_Data/uploads folder
                var path = Path.Combine(Server.MapPath("~/images/products"), tenfile + ".jpg");
                file.SaveAs(path);
                return true;
            }
            // redirect back to the index action to show the form once again
            return false;
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult ThemSP([Bind(Include = "TenSP,LoaiSP,HangSX,XuatXu,GiaGoc,MoTa,SoLuong,isnew,ishot,GioiThieu,ThongSoKyThuat")] SanPham sanpham, HttpPostedFileBase ad, HttpPostedFileBase an, HttpPostedFileBase ak)
        {
            SanPhamModel spm = new SanPhamModel();
            if (ModelState.IsValid)
            {
                string masp = spm.ThemSP(sanpham);
                UploadAnh(ad, masp + "1");
                UploadAnh(an, masp + "2");
                UploadAnh(ak, masp + "3");
                return RedirectToAction("SanPham");
            }
            ViewBag.HangSX = new SelectList(spm.GetAllHangSX(), "HangSX", "TenHang", sanpham.HangSX);
            ViewBag.LoaiSP = new SelectList(spm.GetAllLoaiSP(), "MaLoai", "TenLoai", sanpham.LoaiSP);
            return View("SanPham",sanpham);
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult SPDetail(string id)
        {
            SanPhamModel sp = new SanPhamModel();
            return PartialView("SPDetail", sp.FindById(id));
        }

        [AuthLog(Roles = "Quản trị viên")]
        [HttpPost]
        public ActionResult MultibleDel(List<string> lstdel)
        {
            if (lstdel == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            foreach (var item in lstdel)
            {
                SanPhamModel spm = new SanPhamModel();
                DeleteAnh(spm.FindById(item).AnhDaiDien);
                DeleteAnh(spm.FindById(item).AnhNen);
                DeleteAnh(spm.FindById(item).AnhKhac);
                spm.DeleteSP(item);
            } 
            return TimSP(null,null,null);
        }        

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult TimSP(string key,string maloai,int? page)
        {
            SanPhamModel spm = new SanPhamModel();
            ViewBag.key = key;
            ViewBag.maloai = maloai;
            return PhanTrangSP(spm.AdvancedSearch(key, maloai, null, null, null),page,null);
        }
        //public actionresult timhsx(string key, string maloai, int? page)
        //{
        //    hangsanxuatmodel spm = new hangsanxuatmodel();
        //    viewbag.key = key;
        //    viewbag.maloai = maloai;
        //    return phantrangsp(spm.advancedsearch(key, maloai, null, null, null), page, null);
        //}

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult PhanTrangSP(IQueryable<SanPham> lst,int? page, int? pagesize)
        {
            int pageSize = (pagesize ?? 10);
            int pageNumber = (page ?? 1);
            return PartialView("SanPhamPartial", lst.OrderBy(m => m.MaSP).ToPagedList(pageNumber, pageSize));
        }

        [AuthLog(Roles = "Quản trị viên")]
        public bool DeleteAnh(string filename)
        {
            string fullPath = Request.MapPath("~/images/products/" + filename);
            if (System.IO.File.Exists(fullPath))
            {
                System.IO.File.Delete(fullPath);
                return true;
            }
            return false;
        }
        public bool DownloadAnh(string link, string filename)
        {
            string extend = ".webp";
            using (WebClient webClient = new WebClient())
            {
                webClient.DownloadFile(link, Server.MapPath("~/images/products/" + filename + extend));
                return true;
            }
        }
        public ActionResult AddData()
        {
            SanPhamModel spm = new SanPhamModel();
            using (TextFieldParser parser = new TextFieldParser(Server.MapPath("~/data/database-dongho.csv")))
            {
                parser.TextFieldType = FieldType.Delimited;
                parser.SetDelimiters(",");
                while (!parser.EndOfData)
                {
                    string[] values = parser.ReadFields();
                    if (values[0].Contains("Link")) continue;
                    //Xu ly hang san xuat
                    string hsx = "";
                    if (values[2].Equals("Samsung"))
                        hsx = "30312";
                    else if (values[2].Equals("Apple"))
                        hsx = "52018";
                    else if (values[2].Equals("Huawei"))
                        hsx = "07203";
                    else if (values[2].Equals("Xiaomi"))
                        hsx = "35225";
                    else if (values[2].Equals("Garmin"))
                        hsx = "57235";
                    else if (values[2].Equals("Fitbit"))
                        hsx = "26062";
                    else if (values[2].Equals("Zeblaze"))
                        hsx = "87146";
                    else if (values[2].Equals("Sinophy"))
                        hsx = "87146";
                    else
                    {
                        hsx = values[2].Substring(0, 5).ToUpper();
                    }
                    //Create SanPham
                    SanPham sp = new SanPham();
                    sp.TenSP = values[1];
                    sp.LoaiSP = "70443";
                    sp.HangSX = hsx;
                    sp.XuatXu = "Việt Nam";
                    sp.GiaGoc = decimal.Parse(values[3]);
                    sp.GiaTien = decimal.Parse(values[3]);

                    IEnumerable<string> words = values[4].Split().Take(30);
                    sp.GioiThieu = words.ToString();
                    sp.MoTa = values[4];
                    sp.SoLuong = 20;
                    sp.ishot = false;
                    sp.isnew = false;

                    string masp = spm.ThemSP(sp);
                    DownloadAnh(values[5], masp + "1");
                    DownloadAnh(values[5], masp + "2");
                    DownloadAnh(values[5], masp + "3");
                }
            }
            return RedirectToAction("SanPham");
        }
        public ActionResult DeleteSPLazada()
        {
            using (TextFieldParser parser = new TextFieldParser(Server.MapPath("~/data/database-lazada.csv")))
            {
                parser.TextFieldType = FieldType.Delimited;
                parser.SetDelimiters(",");
                while (!parser.EndOfData)
                {
                    string[] values = parser.ReadFields();
                    if (values[0].Contains("Link")) continue;
                    var x = values[1];
                    SanPhamModel spm = new SanPhamModel();
                    DeleteAnh(spm.FindByName(values[1]).AnhDaiDien);
                    DeleteAnh(spm.FindByName(values[1]).AnhNen);
                    DeleteAnh(spm.FindByName(values[1]).AnhKhac);
                    spm.DeleteSPName(values[1]);

                }
            }
            return RedirectToAction("SanPham");

        }
        public ActionResult AddDataLazada()
        {
            SanPhamModel spm = new SanPhamModel();
            using (TextFieldParser parser = new TextFieldParser(Server.MapPath("~/data/database-lazada.csv")))
            {
                parser.TextFieldType = FieldType.Delimited;
                parser.SetDelimiters(",");
                while (!parser.EndOfData)
                {
                    string[] values = parser.ReadFields();
                    if (values[0].Contains("Link")) continue;
                    //Xu ly hang san xuat

                    //Create SanPham
                    SanPham sp = new SanPham();
                    sp.TenSP = values[1];

                    sp.HangSX = values[2];
                    sp.LoaiSP = values[3];
                    sp.XuatXu = "Việt Nam";
                    sp.GiaGoc = decimal.Parse(values[4]);
                    sp.GiaTien = decimal.Parse(values[4]);

                    //IEnumerable<string> words = values[4].Split().Take(30);
                    //sp.GioiThieu = words.ToString();
                    //sp.MoTa = values[4];
                    sp.SoLuong = 20;
                    sp.ishot = false;
                    sp.isnew = false;

                    string masp = spm.ThemSP(sp);
                    DownloadAnh(values[5], masp + "1");
                    DownloadAnh(values[6], masp + "2");
                    DownloadAnh(values[7], masp + "3");
                }
            }
            return RedirectToAction("SanPham");
        }
    }
}