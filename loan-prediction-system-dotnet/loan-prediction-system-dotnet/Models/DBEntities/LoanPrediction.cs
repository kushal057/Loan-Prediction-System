using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace loan_prediction_system_dotnet.Models
{
    public class LoanPrediction
    {
        [Key]
        public int Id { get; set; }
        public string LoanStatus { get; set; }
        public string Message { get; set; }
        public string Charts { get; set; }

        [ForeignKey("LoanApplicationId")]
        public int LoanApplicationId { get; set; }
        public virtual LoanApplication LoanApplication { get; set; }
    }

}
