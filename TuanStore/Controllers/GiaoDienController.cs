using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using TuanStore.Models;

namespace TuanStore.Controllers
{

    public class GiaoDienController : Controller
    {
        //
        // GET: /GiaoDien/
        public ActionResult Header()
        {
            GiaoDienModel dd = new GiaoDienModel();
            List<GiaoDien> model = dd.GetDD().ToList();
            return View(model);
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên")]
        public ActionResult General()
        {
            GiaoDienModel dd = new GiaoDienModel();
            List<GiaoDien> model = dd.GetDD().ToList();
            return View(model);
        }

        public ActionResult SlideShowView()
        {
            KhuyenMaiModel km = new KhuyenMaiModel();
            return PartialView("SlideShowView", km.TimKhuyenMai(null, null, null).Where(m => m.NgayBatDau <= DateTime.Today && m.NgayKetThuc >= DateTime.Today));
        }
    }
}