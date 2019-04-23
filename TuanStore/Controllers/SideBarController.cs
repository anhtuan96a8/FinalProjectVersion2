using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using TuanStore.Models;

namespace TuanStore.Controllers
{
    public class SideBarController : Controller
    {
        // GET: SlideBar
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult ProductFilter()
        {
            return PartialView("ProductFilter");
        }

        public ActionResult GiamGiaNhieu()
        {
            SanPhamModel sp = new SanPhamModel();
            IQueryable<SanPham> splist = sp.SPKhuyenMai();
            splist = splist.Take(9);
            return PartialView("_GiamGiaNhieuPartial", splist);
        }

        public ActionResult KhuyenMaiPost()
        {
            KhuyenMaiModel km = new KhuyenMaiModel();
            return PartialView("_KhuyenMaiPost",km.TimKhuyenMai(null, null, null).Where(m=> m.NgayBatDau <= DateTime.Today && m.NgayKetThuc >= DateTime.Today));
        }
    }
}