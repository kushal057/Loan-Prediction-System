using loan_prediction_system_dotnet.Areas.Identity.Data;
using loan_prediction_system_dotnet.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using System.Text;
using System.Transactions;

namespace loan_prediction_system_dotnet.Controllers
{
    public class LoanController : Controller
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly AppDBContext _context;
        private readonly UserManager<IdentityUser> _userManager;

        public LoanController(IHttpClientFactory httpClientFactory, AppDBContext context, UserManager<IdentityUser> userManager)
        {
            _httpClientFactory = httpClientFactory;
            _context = context;
            _userManager = userManager;
        }
        public async Task<IActionResult> Index()
        {
            var loanApplications = await _context.LoanApplication.AsQueryable().Where(a => a.UserId == _userManager.GetUserId(User)).ToListAsync();
            List<LoanApplicationModel> model = new List<LoanApplicationModel>() { };
            foreach (var item in loanApplications)
            {
                LoanApplicationModel result = new LoanApplicationModel
                {
                    Id = item.Id,
                    Dataset = new LoanApplicationDataset
                    {
                        Gender = item.Gender,
                        Married = item.Married,
                        Dependents = item.Dependents,
                        Education = item.Education,
                        SelfEmployed = item.SelfEmployed,
                        ApplicantIncome = item.ApplicantIncome,
                        CoapplicantIncome = item.CoapplicantIncome,
                        LoanAmount = item.LoanAmount,
                        LoanAmountTerm = item.LoanAmountTerm,
                        CreditHistory = item.CreditHistory,
                        PropertyArea = item.PropertyArea
                    }
                };

                model.Add(result);

            }
            return View(model);
        }

        public async Task<IActionResult> Submit(LoanApplicationModel model)
        {
            var client = _httpClientFactory.CreateClient();
            var apiUrl = "http://127.0.0.1:5000/predict";

            var loanData = new
            {
                Gender = model.Dataset.Gender,
                Married = model.Dataset.Married,
                Dependents = model.Dataset.Dependents,
                Education = model.Dataset.Education,
                Self_Employed = model.Dataset.SelfEmployed,
                ApplicantIncome = model.Dataset.ApplicantIncome,
                CoapplicantIncome = model.Dataset.CoapplicantIncome,
                Loan_Amount = model.Dataset.LoanAmount,
                Loan_Amount_Term = model.Dataset.LoanAmountTerm,
                Credit_History = model.Dataset.CreditHistory,
                Property_Area = model.Dataset.PropertyArea
            };

            var content = new StringContent(JsonConvert.SerializeObject(loanData), Encoding.UTF8, "application/json");

            try
            {

                var response = await client.PostAsync(apiUrl, content);

                response.EnsureSuccessStatusCode();

                var responseString = await response.Content.ReadAsStringAsync();
                LoanPredictionModel result = JsonConvert.DeserializeObject<LoanPredictionModel>(responseString);

                using (TransactionScope scope = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled))
                {
                    LoanApplication loanApplication = new LoanApplication()
                    {
                        Id = model.Id,
                        Gender = model.Dataset.Gender,
                        Married = model.Dataset.Married,
                        Dependents = model.Dataset.Dependents,
                        Education = model.Dataset.Education,
                        SelfEmployed = model.Dataset.SelfEmployed,
                        ApplicantIncome = model.Dataset.ApplicantIncome,
                        CoapplicantIncome = model.Dataset.CoapplicantIncome,
                        LoanAmount = model.Dataset.LoanAmount,
                        LoanAmountTerm = model.Dataset.LoanAmountTerm,
                        CreditHistory = model.Dataset.CreditHistory,
                        PropertyArea = model.Dataset.PropertyArea,
                        UserId = _userManager.GetUserId(User)
                    };

                    var addLoanApplicationResult = await _context.LoanApplication.AddAsync(loanApplication);
                    await _context.SaveChangesAsync();

                    var addLoanPredictionApplicationResult = await _context.LoanPrediction.AddAsync(new LoanPrediction()
                    {
                        LoanApplicationId = loanApplication.Id,
                        LoanStatus = result.LoanStatus,
                        Message = result.Message,
                        Charts = JsonConvert.SerializeObject(result.Charts)
                    });


                    await _context.SaveChangesAsync();
                    scope.Complete();
                }

                return View("LoanStatus", result);
            }
            catch (Exception ex)
            {
                ViewBag.Error = "Error in fetching data from the API: " + ex.Message;
                return View("LoanStatus", model);
            }
        }

        public async Task<IActionResult> CreateLoanApplication()
        {
            ViewBag.Title = "Create Loan Application";
            return View(new LoanApplicationModel());

        }

        public async Task<IActionResult> GetLoanPredictionByLoanApplicationId(int loanApplicationId)
        {
            var loanPrediction = await _context.LoanPrediction.FirstOrDefaultAsync(a => a.LoanApplicationId == loanApplicationId);
            LoanPredictionModel model = new LoanPredictionModel();
            if (loanPrediction != null)
            {
                model.LoanStatus = loanPrediction.LoanStatus;
                model.Message = loanPrediction.Message;
                model.Charts = JsonConvert.DeserializeObject<Dictionary<string, string>>(loanPrediction.Charts) ?? new Dictionary<string, string>();
            }
            return View(model);
        }

    }
}
