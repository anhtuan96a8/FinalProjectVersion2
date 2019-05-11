using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;

namespace TuanStore.Models
{
    public class UserModel
    {
        Entities db = new Entities();
        internal AspNetUser FindById(string p)
        {
            return db.AspNetUsers.Find(p);
        }

        internal void UpdateInfo(EditInfoModel info, string id)
        {
            AspNetUser user = new AspNetUser();

            user = db.AspNetUsers.Find(id);
            if (user != null)
            {
                user.Email = info.Email;
                user.PhoneNumber = info.DienThoai;
                user.CMND = info.CMND;
                user.HoTen = info.HoTen;
                user.NgaySinh = info.NgaySinh;
                user.GioiTinh = info.GioiTinh;
                user.DiaChi = info.DiaChi;
                db.Entry(user).State = EntityState.Modified;
                db.SaveChanges();
            }
        }
        //internal int TotalUser()
        //{
        //    int total = from p in db.AspNetUsers
        //                where p.AspNetRoles.ToString() =="Khách hàng"
        //                select p.MaNV.Count();
        //    return total;
        //}
        internal void UpdateImage(string p)
        {
            AspNetUser user = new AspNetUser();
            user = db.AspNetUsers.Find(p);
            if (user != null)
            {
                user.Avatar = p + ".jpg";
                db.Entry(user).State = EntityState.Modified;
                db.SaveChanges();
            }
        }

        internal IQueryable<AspNetUser> SearchUser(string key, string email, string hoten, string phone, string quyen)
        {
            IQueryable<AspNetUser> lst = db.AspNetUsers;
            if (!string.IsNullOrEmpty(key))
                lst = lst.Where(m => m.UserName.ToLower().Contains(key.ToLower()));
            if (!string.IsNullOrEmpty(email))
                lst = lst.Where(m => m.Email.ToLower().Contains(email.ToLower()));
            if (!string.IsNullOrEmpty(hoten))
                lst = lst.Where(m => m.HoTen.ToLower().Contains(hoten.ToLower()));
            if (!string.IsNullOrEmpty(phone))
                lst = lst.Where(m => m.PhoneNumber.Contains(phone));
            if (!string.IsNullOrEmpty(quyen))
                lst = lst.Where(m => m.AspNetRoles.FirstOrDefault().Id.Equals(quyen));
            return lst;
        }

        internal IQueryable<AspNetRole> GetAllRole()
        {
            return db.AspNetRoles;
        }

        internal void deleleallrole(string item)
        {
            var user = db.AspNetUsers.Find(item);
            db.Entry(user).Collection("AspNetRoles").Load();
            user.AspNetRoles.Remove(user.AspNetRoles.FirstOrDefault());
            db.SaveChanges();
        }


        internal bool ConfirmMail(string id)
        {
            AspNetUser user = new AspNetUser();

            user = db.AspNetUsers.Find(id);
            if (user != null)
            {
                user.EmailConfirmed = true;
                db.Entry(user).State = EntityState.Modified;
                db.SaveChanges();
                return true;
            }
            return false;
        }

        internal void DeleteUser(string id)
        {
            AspNetUser user = db.AspNetUsers.Find(id);
            db.AspNetUsers.Remove(user);
            db.SaveChanges();
        }

        internal void SendMailConfirm(string p,string url)
        {
            EmailTool sendmail = new EmailTool();
            AspNetUser us = db.AspNetUsers.Find(p);
            if(us != null)
            {
                string mail = us.Email;
                string sub = "[Xác nhận email] Xác nhận đăng ký tại TMDT_J shop";
                string bo = "";
                bo += "Xin chào " + us.HoTen + ",<br>";
                bo += "Cảm ơn bạn đã đăng ký tịa TMDT_Shop, đây là link xác nhận email của bạn <br>";
                bo += "Click vào link bên dưới để xác nhận:<br>";
                bo += "<a href=\""+ url +"\">" + url + "</a><br>";
                bo += "Xin cảm ơn.";
                sendmail.SendMail(new EmailModel(mail, sub, bo));
            }

        }
        internal bool Kiemtraten(string key)
        {
            var temp = db.AspNetUsers.Where(m => m.UserName.Equals(key)).ToList();
            if (temp.Count == 0)
                return true;
            return false;
        }
        internal bool Kiemtraemail(string key)
        {
            var temp = db.AspNetUsers.Where(m => m.Email.Equals(key)).ToList();
            if (temp.Count == 0)
                return true;
            return false;
        }
    }
}