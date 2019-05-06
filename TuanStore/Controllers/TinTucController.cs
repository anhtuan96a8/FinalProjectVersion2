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
    public class TinTucController : Controller
    {
        // GET: TinTuc
        private Entities db = new Entities();
        public ActionResult Index()
        {
            TinTuc tt = new TinTuc();
            return View(tt);
        }
        public ActionResult AddTinTuc()
        {
            return View();
        }
        public ActionResult EditTinTuc()
        {
            return View();
        }
        public ActionResult DeleteTinTuc()
        {
            return View();
        }
        public ActionResult ShowTTForUser()
        {
            
            return View();
        }
    }
}