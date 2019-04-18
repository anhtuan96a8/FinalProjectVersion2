using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(TuanStore.Startup))]
namespace TuanStore
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
