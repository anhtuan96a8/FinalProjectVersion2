﻿using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace TuanStore.Models
{
    public class CommentModel
    {
        private Entities db = new Entities();

        public void AddComment(BinhLuan bl)
        {
            db.BinhLuans.Add(bl);
            db.SaveChanges();
        }

        internal IQueryable<BinhLuan> FindByMaSP(string masp)
        {
            return db.BinhLuans.Where(m => m.MaSP == masp && m.Parent == null);
        }

        internal void UpdateComment(BinhLuan Comment)
        {
            var cmpar = db.BinhLuans.Find(Comment.Parent);
            cmpar.DaTraLoi = "R";
            db.Entry(cmpar).State = EntityState.Modified;
            db.SaveChanges();
            var cm = db.BinhLuans.Find(Comment.MaBL);
            cm.DaTraLoi = "N";
            db.Entry(cm).State = EntityState.Modified;
            db.SaveChanges();
        }

        
        internal IQueryable<BinhLuan> TimBinhLuan(string key, DateTime? date, string status)
        {
            IQueryable<BinhLuan> lst = db.BinhLuans;
            if (!string.IsNullOrEmpty(key))
                lst = lst.Where(m => m.SanPham.TenSP.Contains(key));
            if (date != null)
            {
                lst = lst.Where(m => m.NgayDang.Value.Year == date.Value.Year && m.NgayDang.Value.Month == date.Value.Month && m.NgayDang.Value.Day == date.Value.Day);
            }
            if (!string.IsNullOrEmpty(status))
                lst = lst.Where(m => m.DaTraLoi == status);
            return lst;
        }

        internal void DeleteBinhLuan(int mabl)
        {
            var bl = db.BinhLuans.Find(mabl);
            if (bl == null) return;
            if (bl.DaTraLoi == "R")
            {
                var blchil = db.BinhLuans.Where(m => m.Parent == mabl);
                if (blchil.First() != null)
                {
                    BasicDel(blchil.First().MaBL);
                }
            }
            if (bl.DaTraLoi == "N")
            {
                var blpar = db.BinhLuans.Find(bl.Parent);
                blpar.DaTraLoi = "C";
                db.Entry(blpar).State = EntityState.Modified;
                db.SaveChanges();
            }
            BasicDel(mabl);      
        }
        
        private void BasicDel(int mabl)
        {
            var bl = db.BinhLuans.Find(mabl);
            db.BinhLuans.Remove(bl);
            db.SaveChanges();
        }

        internal BinhLuan FindById(string id)
        {
            throw new NotImplementedException();
        }

        internal IQueryable<BinhLuan> FindChild(int mabl)
        {
            return db.BinhLuans.Where(m => m.Parent == mabl);
        }

        internal AspNetUser GetUser(string id)
        {
            return db.AspNetUsers.Where(m => m.Id == id).FirstOrDefault();
        }
    }
}