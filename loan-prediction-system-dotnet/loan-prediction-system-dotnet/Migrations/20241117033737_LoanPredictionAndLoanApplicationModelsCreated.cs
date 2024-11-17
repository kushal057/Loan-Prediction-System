using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace loan_prediction_system_dotnet.Migrations
{
    public partial class LoanPredictionAndLoanApplicationModelsCreated : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "LoanApplication",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Gender = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Married = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Dependents = table.Column<int>(type: "int", nullable: false),
                    Education = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    SelfEmployed = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ApplicantIncome = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    CoapplicantIncome = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    LoanAmount = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    LoanAmountTerm = table.Column<int>(type: "int", nullable: false),
                    CreditHistory = table.Column<int>(type: "int", nullable: false),
                    PropertyArea = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_LoanApplication", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "LoanApplicationModel",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_LoanApplicationModel", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "LoanPrediction",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    LoanStatus = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Message = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Charts = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    LoanApplicationId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_LoanPrediction", x => x.Id);
                    table.ForeignKey(
                        name: "FK_LoanPrediction_LoanApplication_LoanApplicationId",
                        column: x => x.LoanApplicationId,
                        principalTable: "LoanApplication",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_LoanPrediction_LoanApplicationId",
                table: "LoanPrediction",
                column: "LoanApplicationId");
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "LoanApplicationModel");

            migrationBuilder.DropTable(
                name: "LoanPrediction");

            migrationBuilder.DropTable(
                name: "LoanApplication");
        }
    }
}
