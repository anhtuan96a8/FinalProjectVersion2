using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Web;

namespace TuanStore.Models
{
    public class Chitietgiohang
    {
        public SanPham sanPham { get; set; }
        [DisplayName("Số lượng")]
        public int Soluong { get; set; }
        private double thanhtien;

        public double Thanhtien
        {
            get { return (double)sanPham.GiaTien * Soluong; }
            set { thanhtien = value; }
        }
        public DonHangKH Donhangkh { get; set; }
       
        public void Tinhtien()
        {
            Thanhtien = (double)sanPham.GiaTien * Soluong;
        }
    }
}