using Microsoft.AspNetCore.Identity;
using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace loan_prediction_system_dotnet.Models
{

    public class LoanApplication
    {
        [Key]
        public int Id { get; set; }
        public string Gender { get; set; }
        public string Married { get; set; }
        public int Dependents { get; set; }
        public string Education { get; set; }
        public string SelfEmployed { get; set; }
        public decimal ApplicantIncome { get; set; }
        public decimal CoapplicantIncome { get; set; }
        public decimal LoanAmount { get; set; }
        public int LoanAmountTerm { get; set; }
        public int CreditHistory { get; set; }
        public string PropertyArea { get; set; }

        [ForeignKey("User")]
        public string UserId { get; set; }

        public IdentityUser User { get; set; }
    }
}
