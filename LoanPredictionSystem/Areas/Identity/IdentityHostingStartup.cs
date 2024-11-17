using System;
using LoanPredictionSystem.Areas.Identity.Data;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.UI;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

[assembly: HostingStartup(typeof(LoanPredictionSystem.Areas.Identity.IdentityHostingStartup))]
namespace LoanPredictionSystem.Areas.Identity
{
    public class IdentityHostingStartup : IHostingStartup
    {
        public void Configure(IWebHostBuilder builder)
        {
            builder.ConfigureServices((context, services) => {
                services.AddDbContext<LoanPredictionSystemContext>(options =>
                    options.UseSqlServer(
                        context.Configuration.GetConnectionString("LoanPredictionSystemContextConnection")));

                services.AddDefaultIdentity<IdentityUser>(options => options.SignIn.RequireConfirmedAccount = true)
                    .AddEntityFrameworkStores<LoanPredictionSystemContext>();
            });
        }
    }
}
