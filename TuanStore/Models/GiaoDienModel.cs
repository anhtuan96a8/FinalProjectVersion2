using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TuanStore.Models
{
    public class GiaoDienModel
    {
        private Entities db = new Entities();

        internal IQueryable<GiaoDien> GetDD()
        {
            return db.GiaoDiens;
        }
    }
}