using Newtonsoft.Json;

namespace loan_prediction_system_dotnet.Models
{
    public class LoanPredictionModel
    {
        [JsonProperty("loan_status")]
        public string LoanStatus { get; set; }
        public string Message { get; set; }
        public Dictionary<string, string> Charts { get; set; }
    }

}
