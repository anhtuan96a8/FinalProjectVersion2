using TuanStore.Models;
using PagedList;
using PagedList.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Microsoft.AspNet.Identity;
using TuanStore.Controllers;


namespace TuanStore.Controllers
{
    public class DanhGiaController : Controller
    {
        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult Index()
        {
            return View();
        }
        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult TimDanhGia(string key, DateTime? date,string rate, int? page)
        {
            DanhGiaModel spm = new DanhGiaModel();
            ViewBag.key = key;
            ViewBag.date = date;
            ViewBag.rate = rate;
            return PhanTrangBL(spm.TimDanhGia(key, date,rate), page, null);
        }
        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult PhanTrangBL(IQueryable<DanhGiaSP> lst, int? page, int? pagesize)
        {
            int pageSize = (pagesize ?? 10);
            int pageNumber = (page ?? 1);
            return PartialView("DanhGiaPartial", lst.OrderByDescending(m => m.NgayDang).ToPagedList(pageNumber, pageSize));
        }
        [AllowAnonymous]
        public ActionResult LoadDanhGia(string masp, int? page)
        {
            DanhGiaModel cm = new DanhGiaModel();
            //cai dat phan trang
            //So san pham tren 1 trang
            int pageSize = 10;
            //So trang
            int pageNumber = (page ?? 1);
            ViewBag.masp = masp;
            return PartialView("_ListRatingPartial", cm.FindByMaSP(masp).OrderByDescending(m => m.NgayDang).ToPagedList(pageNumber, pageSize));
        }
        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult DeleteDanhGia(int id)
        {
            DanhGiaModel cm = new DanhGiaModel();
            cm.DeleteDanhGia(id);
            return RedirectToAction("TimDanhGia");
        }
        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        [HttpPost]
        public ActionResult MultibleDel(List<int> lstdel)
        {
            foreach (var item in lstdel)
            {
                DanhGiaModel spm = new DanhGiaModel();
                spm.DeleteDanhGia(item);
            }
            return RedirectToAction("TimDanhGia");
        }
        [AllowAnonymous]
        //Hien thi form de binh luan co tham so la masp va makh
        public ActionResult AddDanhGia(string masp)
        {
            ViewBag.masp = masp;

            string userid = User.Identity.GetUserId();
            if (userid != null)
            {
                UserModel us = new UserModel();
                var user = us.FindById(userid);
                ViewBag.Name = user.UserName;
            }
            return PartialView("_RatingFormPartial");
        }
        [AllowAnonymous]
        //Them binh luan moi sau khi nhan nut gui binh luan se chay ham nay
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult AddDanhGia(DanhGiaSP danhGia)
        {
            danhGia.Rate = 4;
            danhGia.NgayDang = DateTime.Now;
            danhGia.MaKH = User.Identity.GetUserId();
            DanhGiaModel cm = new DanhGiaModel();
            cm.AddDanhGia(danhGia);

            return RedirectToAction("LoadDanhGia", new { masp = danhGia.MaSP });
        }
    }
}