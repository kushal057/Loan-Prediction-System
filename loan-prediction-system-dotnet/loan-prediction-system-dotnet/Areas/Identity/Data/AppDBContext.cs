using loan_prediction_system_dotnet.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using System.Reflection.Emit;

namespace loan_prediction_system_dotnet.Areas.Identity.Data;

public class AppDBContext : IdentityDbContext<IdentityUser>
{
    public AppDBContext(DbContextOptions<AppDBContext> options)
        : base(options)
    {
    }
    public DbSet<LoanApplication> LoanApplication { get; set; }
    public DbSet<LoanPrediction> LoanPrediction { get; set; }    

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        builder.Entity<LoanApplicationModel>().Ignore(la => la.Dataset);
    }
}
