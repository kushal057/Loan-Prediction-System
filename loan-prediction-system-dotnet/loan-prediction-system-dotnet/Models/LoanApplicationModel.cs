using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;

namespace loan_prediction_system_dotnet.Models
{
    public class LoanApplicationModel
    {
        [Key]
        public int Id { get; set; }

        public LoanApplicationDataset Dataset { get; set; }
    }
    public class LoanApplicationDataset
    {
        [JsonProperty("Gender")]
        public string Gender { get; set; }

        [JsonProperty("Married")]
        public string Married { get; set; }

        [JsonProperty("Dependents")]
        public int Dependents { get; set; }

        [JsonProperty("Education")]
        public string Education { get; set; }

        [JsonProperty("Self_Employed")]
        public string SelfEmployed { get; set; }

        [JsonProperty("ApplicantIncome")]
        public decimal ApplicantIncome { get; set; }

        [JsonProperty("CoapplicantIncome")]
        public decimal CoapplicantIncome { get; set; }

        [JsonProperty("Loan_Amount")]
        public decimal LoanAmount { get; set; }

        [JsonProperty("Loan_Amount_Term")]
        [Range(0, int.MaxValue, ErrorMessage = "Loan Amount Term must be a positive value.")]
        public int LoanAmountTerm { get; set; }

        [JsonProperty("Credit_History")]
        public int CreditHistory { get; set; }

        [JsonProperty("Property_Area")]
        public string PropertyArea { get; set; }

    }


}
