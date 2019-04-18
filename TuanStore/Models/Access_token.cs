using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TuanStore.Models
{
    public class Access_token
    {
        public string consumer_key { get; set; }
        public string request_token { get; set; }
        public string verifier_token { get; set; }
    }
}