using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace TuanStore.Models
{
    public class DanhGiaModel
    {
        private Entities db = new Entities();
        private void BasicDel(int madg)
        {
            var dg = db.DanhGiaSPs.Find(madg);
            db.DanhGiaSPs.Remove(dg);
            db.SaveChanges();
        }
        public void AddDanhGia(DanhGiaSP dg)
        {
            db.DanhGiaSPs.Add(dg);
            db.SaveChanges();
        }
        internal IQueryable<DanhGiaSP> FindByMaSP(string masp)
        {
            return db.DanhGiaSPs.Where(m => m.MaSP == masp);
        }
        internal BinhLuan FindById(string id)
        {
            throw new NotImplementedException();
        }
        internal IQueryable<DanhGiaSP> TimDanhGia(string key, DateTime? date,string rate)
        {
            IQueryable<DanhGiaSP> lst = db.DanhGiaSPs;
            if (!string.IsNullOrEmpty(key))
                lst = lst.Where(m => m.SanPham.TenSP.Contains(key));
            if (date != null)
            {
                lst = lst.Where(m => m.NgayDang.Value.Year == date.Value.Year && m.NgayDang.Value.Month == date.Value.Month && m.NgayDang.Value.Day == date.Value.Day);
            }
            if (!string.IsNullOrEmpty(rate))
            {
                int x = Int32.Parse(rate);
                lst = lst.Where(m => m.Rate == x);
            }

            return lst;
        }
        internal void DeleteDanhGia(int madg)
        {
            var bl = db.DanhGiaSPs.Find(madg);
            if (bl == null) return;
            BasicDel(madg);
        }
        internal AspNetUser GetUser(string id)
        {
            return db.AspNetUsers.Where(m => m.Id == id).FirstOrDefault();
        }
    }
}