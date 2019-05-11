using TuanStore.Models;
using Microsoft.AspNet.Identity.EntityFramework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace TuanStore.Controllers
{
    [AuthLog(Roles = "Quản trị viên")]
    public class RolesController : Controller
    {
        ApplicationDbContext context;

        public RolesController()
        {
            context = new ApplicationDbContext(); 
        }

        //
        // GET: /Roles/
        public ActionResult Index()
        {
            var Role = new IdentityRole();
            return View(Role);
        }

        public ActionResult Rolelist()
        {
            var Roles = context.Roles.ToList();
            return View(Roles);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(IdentityRole Role)
        {
            if (Role.Name == null)
            {
                TempData["ErrorCreate"] = "Bạn không được để trống tên Tên Chức Vụ";
                return RedirectToAction("Index");
            }

            if (context.Roles.Where(d => d.Name == Role.Name).FirstOrDefault() != null)
            {
                TempData["ErrorCreate2"] = "Tên chức vụ đã tồn tại";
                return RedirectToAction("Index");
               
            }
            TempData["CreateSuccess"] = "oke";
            context.Roles.Add(Role);
            context.SaveChanges();
            return RedirectToAction("Index");
        }
        public ActionResult DeleteRole(string id)
        {
            if(id == "dc481379-dfae-4d9e-93d8-dce55add3258" || id == "a00f8232-0674-4ac3-8a6b-89bd5ce471da" || id == "37877e60-4cd3-4eb3-8a94-a5d881a81446" || id == "8d050225-c36f-4790-bd7b-28bb044d90b1")
            {
                return RedirectToAction("Index");
            }
            var roleremove = context.Roles.Where(d => d.Id == id).FirstOrDefault();
            context.Roles.Remove(roleremove);
            context.SaveChanges();
            return RedirectToAction("Index");
        }
        [AllowAnonymous]
        public ActionResult KiemTraRole(string key)
        {
            IdentityRole role = new IdentityRole();
            if (context.Roles.Where(d => d.Name.ToLower() == key.ToLower()).FirstOrDefault() == null)
                return Json(true, JsonRequestBehavior.AllowGet);
            return Json(false, JsonRequestBehavior.AllowGet);
        }
    }
}