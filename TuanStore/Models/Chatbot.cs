using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Net;
using System.Collections.Specialized;
using System.Text;

namespace TuanStore.Models
{
    public class Chatbot
    {
        public void ChatbotRep(BinhLuan bl)
        {
            SanPhamModel spmd = new SanPhamModel();
            var sp = spmd.FindById(bl.MaSP);

            String content = GetAnswer(sp.TenSP + " : " + bl.NoiDung);

            BinhLuan rep = new BinhLuan();
            rep.Parent = bl.MaBL;
            rep.NoiDung = content;
            rep.NgayDang = DateTime.Now;
            rep.MaKH = "912a7a6d-b24d-40e7-bfed-726fb822b99d";
            rep.MaSP = bl.MaSP;
            rep.HoTen = "Nguyễn Anh Tuấn";
            rep.Email = "admin@gmail.com";

           

            //
            CommentModel cm = new CommentModel();
            cm.AddComment(rep);
            cm.UpdateComment(rep);
        }
        public string GetAnswer(string question)
        {
            using (var client = new WebClient())
            {
                var values = new NameValueCollection();
                values["Question"] = question;

                var response = client.UploadValues("http://localhost:9874/chatbot", values);

                var responseString = Encoding.UTF8.GetString(response);
                return responseString;
            }
        }
    }

}