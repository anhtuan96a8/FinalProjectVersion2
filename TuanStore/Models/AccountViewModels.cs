﻿using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace TuanStore.Models
{
    public class ExternalLoginConfirmationViewModel
    {
        [Required]
        [Display(Name = "Tên đăng nhập")]
        public string UserName { get; set; }
    }

    public class ManageUserViewModel
    {
        [Required(ErrorMessage = "Nhập mật khẩu hiện tại")]
        [DataType(DataType.Password)]
        [Display(Name = "Mật khẩu hiện tại")]
        public string OldPassword { get; set; }

        [Required(ErrorMessage = "Nhập mật khẩu mới")]
        [StringLength(100, ErrorMessage = "{0} phải ít nhất {2} ký tự.", MinimumLength = 6)]
        [DataType(DataType.Password)]
        [Display(Name = "Mật khẩu mới")]
        public string NewPassword { get; set; }

        [Required(ErrorMessage = "Nhập lại mật khẩu mới")]
        [DataType(DataType.Password)]
        [Display(Name = "Nhập lại mật khẩu")]
        [Compare("NewPassword", ErrorMessage = "Mật khẩu không trùng khớp.")]
        public string ConfirmPassword { get; set; }
    }

    public class LoginViewModel
    {
        [Required(ErrorMessage = "Hãy nhập tên đăng nhập")]
        [Display(Name = "Tên đăng nhập")]
        public string UserName { get; set; }

        [Required(ErrorMessage = "Hãy nhập mật khẩu")]
        [DataType(DataType.Password)]
        [Display(Name = "Mật khẩu")]
        public string Password { get; set; }

        [Display(Name = "Duy trì đăng nhập?")]
        public bool RememberMe { get; set; }
    }

    public class RegisterViewModel
    {
        [Required(ErrorMessage = "Hãy nhập Email của bạn")]
        [Display(Name = "Email")]
        [EmailAddress(ErrorMessage = "Email không đúng dạng")]
        [DataType(DataType.EmailAddress)]
        public string Email { get; set; }

        [Required(ErrorMessage = "Hãy nhập tên đăng nhập của bạn")]
        [Display(Name = "Tên đăng nhập")]
        public string UserName { get; set; }

        [Required(ErrorMessage = "Hãy nhập họ tên của bạn")]
        [Display(Name = "Họ tên")]
        public string HoTen { get; set; }

        [Required(ErrorMessage = "Vui lòng cung cấp số điện thoại", AllowEmptyStrings = false)]
        [RegularExpression(@"(09)\d{8}|(01)\d{9}", ErrorMessage = "Số điện thoại không đúng định dạng.")]
        [Display(Name = "Điện thoại liên lạc")]
        [DataType(DataType.PhoneNumber)]
        public string DienThoai { get; set; }


        [Required(ErrorMessage = "Vui lòng cung cấp địa chỉ", AllowEmptyStrings = false)]
        [Display(Name = "Địa chỉ")]
        public string DiaChi { get; set; }

        [Required(ErrorMessage = "Hãy nhập mật khẩu")]
        [StringLength(100, ErrorMessage = "{0} phải ít nhất {2} ký tự.", MinimumLength = 6)]
        [DataType(DataType.Password)]
        [Display(Name = "Mật khẩu")]
        public string Password { get; set; }

        [Required(ErrorMessage = "Hãy nhập lại mật khẩu")]
        [DataType(DataType.Password)]
        [Display(Name = "Xác nhận mật khẩu")]
        [Compare("Password", ErrorMessage = "Mật khẩu không trùng khớp")]
        public string ConfirmPassword { get; set; }

        
    }
    
    public class ForgotPasswordViewModel
    {
        [Required]
        [EmailAddress]
        [Display(Name = "Email")]
        public string Email { get; set; }
    }
    public class ResetPasswordViewModel
    {
        [Required]
        [EmailAddress]
        [Display(Name = "Email")]
        public string Email { get; set; }


        [Required]
        [StringLength(100, ErrorMessage = "{0} phải ít nhất {2} ký tự.", MinimumLength = 6)]
        [DataType(DataType.Password)]
        [Display(Name = "Mật khẩu")]
        public string Password { get; set; }

        [DataType(DataType.Password)]
        [Display(Name = "Nhập lại mật khẩu")]
        [Compare("Password", ErrorMessage = "Mật khẩu không trùng khớp")]
        public string ConfirmPassword { get; set; }

        public string Code { get; set; }
    }
    public class SendCodeViewModel
    {
        public string SelectedProvider { get; set; }
        public ICollection<System.Web.Mvc.SelectListItem> Providers { get; set; }
        public string ReturnUrl { get; set; }
        public bool RememberMe { get; set; }
    }
    public class VerifyCodeViewModel
    {
        [Required]
        public string Provider { get; set; }

        [Required]
        [Display(Name = "Code")]
        public string Code { get; set; }
        public string ReturnUrl { get; set; }

        [Display(Name = "Remember this browser?")]
        public bool RememberBrowser { get; set; }

        public bool RememberMe { get; set; }
    }
    [MetadataTypeAttribute(typeof(DonHangKH.Metadata))]
    public partial class DonHangKH
    {
        internal sealed class Metadata
        {
            [Required(ErrorMessage = "Vui lòng cung cấp số điện thoại", AllowEmptyStrings = false)]
            [RegularExpression(@"(09)\d{8}|(01)\d{9}", ErrorMessage = "Entered phone format is not valid.")]
            [Display(Name = "Điện thoại liên lạc")]
            [DataType(DataType.PhoneNumber)]
            public string Dienthoai { get; set; }
        }
    }

    public class EditInfoModel
    {
        [EmailAddress(ErrorMessage = "Email không đúng dạng")]
        [DataType(DataType.EmailAddress)]
        [Display(Name = "Email")]
        public string Email { get; set; }

        //[Required(ErrorMessage = "Vui lòng cung cấp số điện thoại", AllowEmptyStrings = false)]
        [RegularExpression(@"(09)\d{8}|(01)\d{9}", ErrorMessage = "Entered phone format is not valid.")]
        [Display(Name = "Điện thoại liên lạc")]
        [DataType(DataType.PhoneNumber)]
        public string DienThoai { get; set; }

        //[Required(ErrorMessage = "Vui lòng cung cấp họ tên của bạn", AllowEmptyStrings = false)]
        [Display(Name = "Họ tên")]
        public string HoTen { get; set; }

        [DataType(DataType.Date)]
        [DisplayFormat(ApplyFormatInEditMode = true, DataFormatString = "{0:yyyy-MM-dd}")]
        [Display(Name = "Ngày sinh")]
        public Nullable<System.DateTime> NgaySinh { get; set; }

        [Display(Name = "Giới tính")]
        public Nullable<bool> GioiTinh { get; set; }

        [Display(Name = "Địa chỉ")]
        public string DiaChi { get; set; }

        [Display(Name = "Ảnh đại diện")]
        public string Avatar { get; set; }

        [Display(Name = "Số CMND")]
        public string CMND { get; set; }

        public EditInfoModel() {}

        public EditInfoModel(AspNetUser u)
        {
            Email = u.Email;
            DienThoai = u.PhoneNumber;
            CMND = u.CMND;
            HoTen = u.HoTen;
            NgaySinh = u.NgaySinh;
            GioiTinh = u.GioiTinh;
            DiaChi = u.DiaChi;
            Avatar = u.Avatar;
        }

    }
    
}
