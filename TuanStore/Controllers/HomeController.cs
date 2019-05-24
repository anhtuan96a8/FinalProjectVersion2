using TuanStore.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Microsoft.AspNet.Identity;

namespace TuanStore.Controllers
{
    public class HomeController : Controller
    {
        private static Entities db = new Entities();

        public ActionResult Index()
        {
            ManagerObiect.getIntance();
            
            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
        
        public ActionResult Cart()
        {
            return View(ManagerObiect.getIntance().giohang);
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên,Khách hàng")]
        //Đơn hàng
        public ActionResult Xemdonhang(string maKH)
        {
            List<DonhangKHModel> temp = new List<DonhangKHModel>();
            if (maKH.Length != 0)
            {
                DonhangKHModel dh = new DonhangKHModel();
                temp = dh.Xemdonhang(maKH);
            }
            return View(temp);
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên,Khách hàng")]
        public ActionResult Huydonhang(string maDH)
        {
            DonhangKHModel dh = new DonhangKHModel();
            dh.HuyDH(maDH);
            var donhang = dh.Xemdonhang(User.Identity.GetUserId());
            return View(donhang);
        }
        public ActionResult Checkout()
        {
            if (Request.IsAuthenticated)
            {
                DonhangKHModel dh = new DonhangKHModel();
                dh.nguoiMua = dh.Xemttnguoidung(User.Identity.GetUserId());
                Donhangtongquan dhtq = new Donhangtongquan()
                {
                    buyer = dh.nguoiMua.HoTen,
                    seller = dh.nguoiMua.HoTen,
                    phoneNumber = dh.nguoiMua.PhoneNumber,
                    address = dh.nguoiMua.DiaChi
                };
                return View(dhtq);
            }
            else
            {
                return RedirectToAction("Authentication", "Account", new { returnUrl = "/Home/Checkout" });
            }
        }

        [AuthLog(Roles = "Quản trị viên,Nhân viên,Khách hàng")]
        [HttpPost]
        public ActionResult Checkout(Donhangtongquan dh)
        {
            if (User.Identity.IsAuthenticated)
            {
                DonhangKHModel dhmodel = new DonhangKHModel();
                if (ManagerObiect.getIntance().giohang.getGiohang().Count() != 0)
                {
                    dhmodel.Luudonhang(dh, User.Identity.GetUserId(), ManagerObiect.getIntance().giohang);

                }
                else
                {
                   TempData["alert"] = "Bạn chưa có sản phẩm nào";
                   return RedirectToAction("Checkout", "Home");
                }
                ManagerObiect.getIntance().giohang.removerCarts();
                return RedirectToAction("Xemdonhang", "Home",new { maKH = User.Identity.GetUserId()});
            }
            else
            {
                return RedirectToAction("Checkout", "Home");
            }
        }

        public ActionResult MainMenu()
        {
            MainMenuModel mnmodel = new MainMenuModel();
            var menulist = mnmodel.GetMenuList();
            return PartialView("_MainMenuPartial", menulist);
        }

        public ActionResult SPNoiBat(int? skip)
        {
            SanPhamModel sp = new SanPhamModel();
            int skipnum = (skip+4 ?? 0);
            IQueryable<SanPham> splist = sp.SPHot();
            if (skipnum == 0)
            {
                splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(8);

            }
            else splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(4); if (splist.Any())
                return PartialView("_ProductTabLoadMorePartial", splist);
            else
                return null;
        }

        public ActionResult SPMoiNhap(int? skip)
        {
            SanPhamModel sp = new SanPhamModel();
            int skipnum = (skip+4 ?? 0);
            IQueryable<SanPham> splist = sp.SPMoiNhap();
            if(skipnum == 0)
            {
                splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(8);

            }
            else splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(4);
            if (splist.Any())
                return PartialView("_ProductTabLoadMorePartial", splist);
            else
                return null;
        }
        public ActionResult AllProducts(int? skip)
        {
            SanPhamModel sp = new SanPhamModel();
            int skipnum = (skip ?? 0);
            IQueryable<SanPham> splist = sp.GetAll();
            if (skipnum == 0)
            {
                splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(8);

            }
            else splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(8);
            if (splist.Any())
                return PartialView("_ProductTabLoadMorePartial", splist);
            else
                return null;
        }

        public ActionResult SPKhuyenMai(int? skip)
        {
            SanPhamModel sp = new SanPhamModel();
            int skipnum = (skip+4 ?? 0);
            IQueryable<SanPham> splist = sp.SPKhuyenMai();
            if (skipnum == 0)
            {
                splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(8);

            }
            else splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(4);
            if (splist.Any())
                return PartialView("_ProductTabLoadMorePartial", splist);
            else
                return null;
        }

        public ActionResult SPBanChay()
        {
            SanPhamModel sp = new SanPhamModel();
            IQueryable<SanPham> splist = sp.SPBanChay(7);      
            if (splist.Any())
                return PartialView("_BestSellerPartial", splist.ToList());
            else
                return null;
        }
        public ActionResult SPBanChayLoadMore(int? skip)
        {
            SanPhamModel sp = new SanPhamModel();
            int skipnum = (skip ?? 0);
            IQueryable<SanPham> splist = sp.SPBanChay(skipnum+7);
            if (skipnum == 4)
            {
                splist = splist.OrderBy(r => r.MaSP).Skip(7).Take(4);

            }
            else splist = splist.OrderBy(r => r.MaSP).Skip(skipnum).Take(4);
            if (splist.Any())
                return PartialView("_ProductTabLoadMorePartial", splist);
            else
                return null;
        }
        public ActionResult SPMoiXem()
        {
            return PartialView("_RecentlyViewPartial", ManagerObiect.getIntance().Laydanhsachsanphammoixem());
        }

    }
}