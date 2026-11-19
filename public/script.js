
$(document).ready(function () {

    loadHistory();

    $("#emiForm").submit(function (event) {

        event.preventDefault();

        const P = Number($("#amount").val());
        const rate = Number($("#rate").val());
        const n = Number($("#months").val());

        $("#error").hide();

        // Client-side validation
        if (
            !Number.isFinite(P) || P <= 0 ||
            !Number.isFinite(rate) || rate <= 0 ||
            !Number.isInteger(n) || n <= 0
        ) {
            $("#error").text("Please enter positive valid numbers.")
                       .show();
            return;
        }

        // AJAX POST request
        $.ajax({
            url: "/api/emi",
            method: "POST",
            contentType: "application/json",

            data: JSON.stringify({
                P: P,
                rate: rate,
                n: n
            }),

            success: function (response) {

                $("#emi").text(response.emi.toLocaleString());
                $("#totalPayment").text(
                    response.totalPayment.toLocaleString()
                );
                $("#totalInterest").text(
                    response.totalInterest.toLocaleString()
                );
                $("#servedBy").text(response.servedBy);
                $("#ipAddress").text(response.ipAddress);

                $("#result").show();

                loadHistory();
            },

            error: function (xhr) {
                const message = xhr.responseJSON?.error ||
                                "Unable to calculate EMI.";

                $("#error").text(message).show();
            }
        });

    });

    // Load last 10 calculations
    function loadHistory() {

        $.ajax({
            url: "/api/history",
            method: "GET",

            success: function (data) {

                let rows = "";

                data.forEach(function (item) {

                    rows += `
                        <tr>
                            <td>${Number(item.principal).toLocaleString()}</td>
                            <td>${item.rate}</td>
                            <td>${item.months}</td>
                            <td>${Number(item.emi).toLocaleString()}</td>
                            <td>${$("<div>").text(item.servedBy).html()}</td>
                        </tr>
                    `;
                });

                $("#history").html(rows);
            },

            error: function () {
                $("#history").html(
                    '<tr><td colspan="5">Unable to load history</td></tr>'
                );
            }
        });
    }

});

