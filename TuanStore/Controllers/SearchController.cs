using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using TuanStore.Models;
using PagedList;
using PagedList.Mvc;
using Newtonsoft.Json.Linq;

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
        //public ActionResult Sort(string jsonsort)
        //{
        //    dynamic item = JObject.Parse(jsonsort);
        //    var term = jsonsort.prop1;
        //    return AdvancedSearchP(null, null, null, null);
        //}
        public ActionResult AdvancedSearchP(string term, string loai, string hangsx, string typeview, int? page, int? minprice, int? maxprice,int? typepagelist, int? typesearch ,int? typesort)
        {
            ViewBag.Name = term;
            ViewBag.loai = loai;
            ViewBag.hangsx = hangsx;
            ViewBag.minprice = minprice;
            ViewBag.maxprice = maxprice;
            ViewBag.type = typeview;
            ViewBag.typesearch = typesearch;
            ViewBag.typesort = typesort;
            ViewBag.page= page;
            ViewBag.typepagelist = typepagelist;
            
            // Phân loại search và sort
            SanPhamModel sp = new SanPhamModel();
            IQueryable<SanPham> lst;
            int loaisearch = (typesearch ?? 0);// kiểu search là null thì sẽ là 0
            if(loaisearch == 0)
            {
                lst = sp.AdvancedSearch(term, loai, hangsx, minprice, maxprice);
                if (typesort == 1)
                {
                    lst = lst.OrderBy(e => e.GiaTien);
                }
                else if(typesort == 2)
                {
                    lst = lst.OrderByDescending(e => e.GiaTien);
                }
                else lst = lst.OrderByDescending(m => m.MaSP);
            }
            else if (loaisearch == 1)
            {
                lst = sp.SPKhuyenMai();
                if (typesort == 1)
                {
                    lst = lst.OrderBy(e => e.GiaTien);
                }
                else if (typesort == 2)
                {
                    lst = lst.OrderByDescending(e => e.GiaTien);
                }
                else lst = lst.OrderByDescending(m => m.MaSP);
            }
            else if(loaisearch == 2)
            {
                lst = sp.SPBanChay(0);
                if (typesort == 1)
                {
                    lst = lst.OrderBy(e => e.GiaTien);
                }
                else if (typesort == 2)
                {
                    lst = lst.OrderByDescending(e => e.GiaTien);
                }
                else lst = lst.OrderByDescending(m => m.MaSP);
            }
            else if(loaisearch == 3)
            {
                lst = sp.SPHot();
                if (typesort == 1)
                {
                    lst = lst.OrderBy(e => e.GiaTien);
                }
                else if (typesort == 2)
                {
                    lst = lst.OrderByDescending(e => e.GiaTien);
                }
                else lst = lst.OrderByDescending(m => m.MaSP);
            }
            else if (loaisearch == 4)
            {
                lst = sp.SPMoiNhap();
                if (typesort == 1)
                {
                    lst = lst.OrderBy(e => e.GiaTien);
                }
                else if (typesort == 2)
                {
                    lst = lst.OrderByDescending(e => e.GiaTien);
                }
                else lst = lst.OrderByDescending(m => m.MaSP);
            }
            else
            {
                lst = ManagerObiect.getIntance().Laydanhsachsanphammoixem().AsQueryable();
                if (typesort == 1)
                {
                    lst = lst.OrderBy(e => e.GiaTien);
                }
                else if (typesort == 2)
                {
                    lst = lst.OrderByDescending(e => e.GiaTien);
                }
                else lst = lst.OrderByDescending(m => m.MaSP);
            }
            // xét phân trang
            int typePT = (typepagelist ?? 0);
            if(typePT == 1)
            {
                return PhanTrangAdvanced2(lst, page);
            }
            else return PhanTrangAdvanced(lst, page);
        }
        
        private ActionResult PhanTrangAdvanced(IQueryable<SanPham> lst, int? page)
        {
            int pageSize = 9;
            int pageNumber = (page ?? 1);
            return View("_AdvancedSearchPartial", lst.ToPagedList(pageNumber, pageSize));
        }
        private ActionResult PhanTrangAdvanced2(IQueryable<SanPham> lst, int? page)
        {
            int pageSize = 9;
            int pageNumber = (page ?? 1);
            return View("_ListProductAjaxPartial", lst.ToPagedList(pageNumber, pageSize));
        }
    }
}