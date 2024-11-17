using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace loan_prediction_system_dotnet.Migrations
{
    public partial class LoanApplicationUserId : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "UserId",
                table: "LoanApplication",
                type: "nvarchar(450)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.CreateIndex(
                name: "IX_LoanApplication_UserId",
                table: "LoanApplication",
                column: "UserId");

            migrationBuilder.AddForeignKey(
                name: "FK_LoanApplication_AspNetUsers_UserId",
                table: "LoanApplication",
                column: "UserId",
                principalTable: "AspNetUsers",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_LoanApplication_AspNetUsers_UserId",
                table: "LoanApplication");

            migrationBuilder.DropIndex(
                name: "IX_LoanApplication_UserId",
                table: "LoanApplication");

            migrationBuilder.DropColumn(
                name: "UserId",
                table: "LoanApplication");
        }
    }
}
