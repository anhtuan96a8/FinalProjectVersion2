using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using TuanStore.Models;
using PagedList;
using PagedList.Mvc;

namespace TuanStore.Controllers
{
    public class SearchController : Controller
    {
        public ActionResult SearchForm()
        {
            return PartialView("_SearchFormPartial");
        }
        public ActionResult CategoryList()
        {
            CategoryModel cat = new CategoryModel();
            var lst = cat.GetCategory().ToList();
            return PartialView("_CategoryListPartial", lst);
        }
        public ActionResult GetHangSanXuat()
        {
            CategoryModel cat = new CategoryModel();
            var lst = cat.GetHangSanXuats().ToList();
            return PartialView("_GetHangSanXuatPartial", lst);
        }

        [HttpPost]
        public ActionResult SearchByName(string term)
        {
            SanPhamModel sp = new SanPhamModel();
            IQueryable<SanPham> lst = sp.SearchByName(term);
            var splist = (from p in lst orderby p.MaSP descending select new { p.MaSP, p.TenSP, p.GiaTien, p.AnhDaiDien }).Take(5);
            return Json(splist, JsonRequestBehavior.AllowGet);
        }

        public ActionResult AdvancedSearchView(string term, string loai, string hangsx, int? minprice, int? maxprice)
        {
            ViewBag.Name = term;
            ViewBag.loai = loai;
            ViewBag.hangsx = hangsx;
            ViewBag.minprice = minprice;
            ViewBag.maxprice = maxprice;
            return View("AdvancedSearchView");
        }

        public ActionResult AdvancedSearchP(string term, string loai, string hangsx, string typeview, int? page, int? minprice, int? maxprice)
        {
            ViewBag.Name = term;
            ViewBag.loai = loai;
            ViewBag.hangsx = hangsx;
            ViewBag.minprice = minprice;
            ViewBag.maxprice = maxprice;
            ViewBag.type = typeview;
            SanPhamModel sp = new SanPhamModel();
            IQueryable<SanPham> lst = sp.AdvancedSearch(term, loai, hangsx, minprice, maxprice);
            return PhanTrangAdvanced(lst, page);
        }

        private ActionResult PhanTrangAdvanced(IQueryable<SanPham> lst, int? page)
        {
            int pageSize = 9;
            int pageNumber = (page ?? 1);
            lst = lst.OrderByDescending(m => m.MaSP);
            return View("_AdvancedSearchPartial", lst.ToPagedList(pageNumber, pageSize));
        }
    }
}