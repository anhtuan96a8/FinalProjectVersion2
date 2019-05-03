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
        public ActionResult Create(IdentityRole Role)
        {
            if (Role.Name == null)
            {
                ViewBag.Message = "Bạn không được để trống tên Tên Chức Vụ";
                return RedirectToAction("Index");
            }

            if (context.Roles.Where(d => d.Name == Role.Name).FirstOrDefault() != null)
            {
                ViewBag.Message = "Tên chức vụ đã tồn tại";
                return RedirectToAction("Index");
               
            }
            context.Roles.Add(Role);
            context.SaveChanges();
            return RedirectToAction("Index");
        }
        public ActionResult DeleteRole(string roleId)
        {
            if(roleId == "dc481379-dfae-4d9e-93d8-dce55add3258")
            {
                return RedirectToAction("Index");
            }
            var roleremove = context.Roles.Where(d => d.Id == roleId).FirstOrDefault();
            context.Roles.Remove(roleremove);
            context.SaveChanges();
            return RedirectToAction("Index");
        }
	}
}