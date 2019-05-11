using TuanStore.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using PagedList;
using PagedList.Mvc;
using System.Net;

namespace TuanStore.Controllers
{
    [AuthLog(Roles = "Quản trị viên,Nhân viên")]
    public class DonhangController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult TimDonHang(string key,string hoten, string mobile, DateTime? date, int? status, int? page)
        {
            DonhangKHModel spm = new DonhangKHModel();
            ViewBag.key = key;
            ViewBag.date = date;
            ViewBag.status = status;
            ViewBag.mobile = mobile;
            ViewBag.hoten = hoten;
            return PhanTrangDH(spm.TimDonHang(key,hoten, mobile, date, status), page, null);
        }
        public ActionResult DeleteDH(string id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            DonhangKHModel donhang = new DonhangKHModel();
            donhang.DeleteDH(id);
            return TimDonHang(null, null, null, null, null,null);
        }
        [HttpPost]
        public ActionResult UpdateTinhTrangDH(string madh, int? tt)
        {
            DonhangKHModel dh = new DonhangKHModel();
            dh.UpdateTinhTrang(madh, tt);
            return RedirectToAction("TimDonHang");
        }

        [HttpPost]
        public ActionResult MultibleUpdate(List<string> lst, int? tt)
        {
            foreach (var item in lst)
            {
                UpdateTinhTrangDH(item, tt);
            }
            return RedirectToAction("TimDonHang");
        }

        public ActionResult PhanTrangDH(IQueryable<DonHangKH> lst, int? page, int? pagesize)
        {
            int pageSize = (pagesize ?? 10);
            int pageNumber = (page ?? 1);
            return PartialView("DonHangPartial", lst.OrderBy(m => m.TinhTrangDH).ToPagedList(pageNumber, pageSize));
        }

        // GET: Donhang
        public ActionResult Chitietdonhang(string id)
        {
            DonhangKHModel ctdh = new DonhangKHModel();
            return PartialView("DonHangDetail",ctdh.ChiTietDonHang(id));
        }
    }
}