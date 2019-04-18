using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.EntityFramework;
using System;
using System.ComponentModel;
using System.Security.Claims;
using System.Threading.Tasks;

namespace TuanStore.Models
{
    // You can add profile data for the user by adding more properties to your ApplicationUser class, please visit http://go.microsoft.com/fwlink/?LinkID=317594 to learn more.
    public class ApplicationUser : IdentityUser
    {
        public async Task<ClaimsIdentity> GenerateUserIdentityAsync(UserManager<ApplicationUser> manager, string authenticationType)
        {
            // Note the authenticationType must match the one defined in CookieAuthenticationOptions.AuthenticationType
            var userIdentity = await manager.CreateIdentityAsync(this, authenticationType);
            // Add custom user claims here
            return userIdentity;
        }
        [DisplayName("Họ và tên")]
        public string HoTen { get; set; }
        [DisplayName("Ngày sinh")]
        public Nullable<System.DateTime> NgaySinh { get; set; }
        [DisplayName("Giới tính")]
        public Nullable<bool> GioiTinh { get; set; }
        [DisplayName("Địa chỉ")]
        public string DiaChi { get; set; }
        public string Avatar { get; set; }
        [DisplayName("Chứng minh thư")]
        public string CMND { get; set; }
    }

    public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
    {
        public ApplicationDbContext()
            : base("DefaultConnection", throwIfV1Schema: false)
        {
        }

        protected override void OnModelCreating(System.Data.Entity.DbModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<ApplicationUser>().ToTable("AspNetUsers");
        }

        public static ApplicationDbContext Create()
        {
            return new ApplicationDbContext();
        }
    }
}