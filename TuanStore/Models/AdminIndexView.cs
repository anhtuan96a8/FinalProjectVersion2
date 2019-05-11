using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TuanStore.Models
{
    public class AdminIndexView
    {
        public int numOfUser;
        public int numOfSuccesfulOrder;
        public double? numOfRevenue;
        public int numOfComment;

        private Entities db = new Entities();
        public AdminIndexView()
        {
            numOfUser = db.AspNetUsers.Count();
            numOfSuccesfulOrder = db.DonHangKHs.Where(o => o.TinhTrangDH == 3).Count();
            numOfRevenue = db.DonHangKHs.Where(o => o.TinhTrangDH == 3).Sum(m => m.Tongtien);
            numOfComment = db.BinhLuans.Count();
        }
    }
}